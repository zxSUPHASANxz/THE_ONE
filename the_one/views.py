from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils import timezone


def home_view(request):
    """Home page view"""
    return render(request, 'home.html')


def login_view(request):
    """Login page view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'ยินดีต้อนรับ {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    
    return render(request, 'auth/login.html')


def register_view(request):
    """Register page view"""
    if request.method == 'POST':
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type', 'customer')
        
        if password != password2:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้มีอยู่แล้ว')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'อีเมลนี้มีอยู่แล้ว')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type
            )
            login(request, user)
            messages.success(request, 'สมัครสมาชิกเรียบร้อยแล้ว!')
            return redirect('home')
    
    return render(request, 'auth/register.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('home')


@login_required
def profile_view(request):
    """Profile page view"""
    from booking.models import Motorcycle
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # Update basic info
            request.user.email = request.POST.get('email')
            request.user.phone_number = request.POST.get('phone_number', '')
            request.user.address = request.POST.get('address', '')
            
            # Handle password change
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if current_password and new_password:
                if new_password != confirm_password:
                    messages.error(request, 'รหัสผ่านใหม่ไม่ตรงกัน')
                elif not request.user.check_password(current_password):
                    messages.error(request, 'รหัสผ่านปัจจุบันไม่ถูกต้อง')
                elif len(new_password) < 6:
                    messages.error(request, 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร')
                else:
                    request.user.set_password(new_password)
                    messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว กรุณาเข้าสู่ระบบใหม่')
                    request.user.save()
                    logout(request)
                    return redirect('login')
            
            try:
                request.user.save()
                messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว!')
            except Exception as e:
                messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
        
        elif action == 'add_motorcycle':
            if not request.user.is_mechanic:
                try:
                    Motorcycle.objects.create(
                        owner=request.user,
                        brand=request.POST.get('brand'),
                        model=request.POST.get('model'),
                        year=request.POST.get('year'),
                        cc=request.POST.get('cc'),
                        license_plate='',
                        bike_type='big_bike'
                    )
                    messages.success(request, 'เพิ่มข้อมูลรถเรียบร้อยแล้ว!')
                except Exception as e:
                    messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
        
        elif action == 'delete_motorcycle':
            if not request.user.is_mechanic:
                try:
                    motorcycle_id = request.POST.get('motorcycle_id')
                    motorcycle = Motorcycle.objects.get(id=motorcycle_id, owner=request.user)
                    motorcycle.delete()
                    messages.success(request, 'ลบข้อมูลรถเรียบร้อยแล้ว!')
                except Motorcycle.DoesNotExist:
                    messages.error(request, 'ไม่พบข้อมูลรถ')
                except Exception as e:
                    messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
        
        return redirect('profile')
    
    # Get motorcycles for customer
    motorcycles = []
    if not request.user.is_mechanic:
        motorcycles = Motorcycle.objects.filter(owner=request.user).order_by('-created_at')
    
    return render(request, 'auth/profile.html', {
        'motorcycles': motorcycles
    })


@login_required
def chatbot_view(request):
    """Chatbot page view"""
    return render(request, 'chatbot/chat.html')


@login_required
def booking_list_view(request):
    """Booking list page view"""
    from booking.models import Booking
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'booking/list.html', {'bookings': bookings})


@login_required
def booking_create_view(request):
    """Booking create page view"""
    from booking.models import Motorcycle, Booking
    from mechanics.models import WorkQueue
    from django.contrib.auth import get_user_model
    import datetime
    from django.utils import timezone
    
    if request.method == 'POST':
        motorcycle_id = request.POST.get('motorcycle')
        problem_description = request.POST.get('problem_description')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')
        
        try:
            motorcycle = Motorcycle.objects.get(id=motorcycle_id, owner=request.user)
            
            # Combine date and time
            appointment_datetime = timezone.make_aware(
                datetime.datetime.strptime(
                    f"{appointment_date} {appointment_time}", 
                    "%Y-%m-%d %H:%M"
                )
            )
            
            booking = Booking.objects.create(
                customer=request.user,
                motorcycle=motorcycle,
                problem_description=problem_description,
                appointment_date=appointment_datetime,
                status='pending'
            )
            
            # Auto-assign to available mechanics
            User = get_user_model()
            mechanics = User.objects.filter(user_type='mechanic')
            
            for mechanic in mechanics:
                WorkQueue.objects.create(
                    mechanic=mechanic,
                    booking=booking,
                    status='pending',
                    priority='medium'
                )
            
            messages.success(request, 'จองคิวเรียบร้อยแล้ว!')
            return redirect('booking_list')
        except Exception as e:
            messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
    
    motorcycles = Motorcycle.objects.filter(owner=request.user)
    return render(request, 'booking/create.html', {'motorcycles': motorcycles})


@login_required
def motorcycle_list_view(request):
    """Motorcycle list page view"""
    from booking.models import Motorcycle
    
    if request.method == 'POST':
        try:
            Motorcycle.objects.create(
                owner=request.user,
                brand=request.POST.get('brand'),
                model=request.POST.get('model'),
                year=request.POST.get('year'),
                cc=request.POST.get('cc'),
                license_plate=request.POST.get('license_plate'),
                bike_type='big_bike'
            )
            messages.success(request, 'เพิ่มข้อมูลรถเรียบร้อยแล้ว!')
        except Exception as e:
            messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
        return redirect('motorcycle_list')
    
    motorcycles = Motorcycle.objects.filter(owner=request.user)
    return render(request, 'booking/motorcycles.html', {'motorcycles': motorcycles})


@login_required
def mechanic_dashboard_view(request):
    """Mechanic dashboard view"""
    from mechanics.models import WorkQueue, Review, MechanicProfile
    from django.db.models import Avg
    from datetime import date
    from booking.models import Booking
    
    # Check if user is mechanic
    if request.user.user_type != 'mechanic':
        messages.error(request, 'คุณไม่มีสิทธิ์เข้าถึงหน้านี้')
        return redirect('home')
    
    # Create MechanicProfile if not exists
    profile, created = MechanicProfile.objects.get_or_create(
        user=request.user,
        defaults={'specialization': 'all', 'years_of_experience': 0}
    )
    
    # Handle form submissions
    if request.method == 'POST':
        action = request.POST.get('action')
        queue_id = request.POST.get('queue_id')
        
        try:
            queue = WorkQueue.objects.get(id=queue_id, mechanic=request.user)
            
            if action == 'accept':
                queue.status = 'in_progress'
                queue.started_at = timezone.now()
                queue.save()
                messages.success(request, 'รับงานเรียบร้อยแล้ว!')
                
            elif action == 'update':
                repair_notes = request.POST.get('repair_notes')
                estimated_cost = request.POST.get('estimated_cost')
                
                queue.booking.repair_notes = repair_notes
                if estimated_cost:
                    queue.booking.estimated_cost = float(estimated_cost)
                queue.booking.save()
                messages.success(request, 'บันทึกข้อมูลแล้ว!')
                
            elif action == 'complete':
                repair_notes = request.POST.get('repair_notes')
                estimated_cost = request.POST.get('estimated_cost')
                
                queue.booking.repair_notes = repair_notes
                if estimated_cost:
                    queue.booking.estimated_cost = float(estimated_cost)
                queue.booking.status = 'completed'
                queue.booking.save()
                
                queue.status = 'completed'
                queue.completed_at = timezone.now()
                queue.save()
                messages.success(request, 'งานเสร็จสิ้นแล้ว!')
                
        except WorkQueue.DoesNotExist:
            messages.error(request, 'ไม่พบงานนี้')
        except Exception as e:
            messages.error(request, f'เกิดข้อผิดพลาด: {str(e)}')
            
        return redirect('mechanic_dashboard')
    
    # Get work queues for this mechanic
    work_queues = WorkQueue.objects.filter(
        mechanic=request.user
    ).select_related(
        'booking', 'booking__customer', 'booking__motorcycle'
    ).order_by('-assigned_at')
    
    # Calculate stats
    pending_count = work_queues.filter(status='pending').count()
    in_progress_count = work_queues.filter(status='in_progress').count()
    completed_today = work_queues.filter(
        status='completed', 
        completed_at__date=date.today()
    ).count()
    
    # Get average rating
    avg_rating = Review.objects.filter(
        mechanic=request.user
    ).aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    
    context = {
        'work_queues': work_queues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_today': completed_today,
        'average_rating': avg_rating,
        'mechanic_profile': profile
    }
    
    return render(request, 'mechanics/dashboard.html', context)
