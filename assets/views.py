from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from .models import Asset, Department, AssetCategory, AssetMovement, MaintenanceRecord
from .forms import AssetForm, MovementForm, MaintenanceForm


# -------------------------------
# Login View
# -------------------------------
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html')


# -------------------------------
# Logout View
# -------------------------------
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')




# -------------------------------
# Updated Dashboard View with Enhanced Analytics
# -------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Asset, Department, AssetCategory, AssetMovement, MaintenanceRecord

@login_required
def dashboard(request):
    # --- Basic Counts ---
    total_assets = Asset.objects.count()
    assets_in_use = Asset.objects.filter(status="In Use").count()
    assets_available = Asset.objects.filter(status="Available").count()
    assets_under_maintenance = Asset.objects.filter(status="Under Maintenance").count()
    assets_disposed = Asset.objects.filter(status="Disposed").count()
    department_count = Department.objects.count()
    category_count = AssetCategory.objects.count()
    
    # Calculate percentages for status
    if total_assets > 0:
        in_use_percentage = round((assets_in_use / total_assets) * 100, 1)
        maintenance_percentage = round((assets_under_maintenance / total_assets) * 100, 1)
        available_percentage = round((assets_available / total_assets) * 100, 1)
    else:
        in_use_percentage = maintenance_percentage = available_percentage = 0

    # --- Assets by Status (for Pie Chart) ---
    assets_by_status = (
        Asset.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )
    status_labels = [item['status'] for item in assets_by_status]
    status_data = [item['total'] for item in assets_by_status]

    # --- Assets by Condition (for Doughnut Chart) ---
    assets_by_condition = (
        Asset.objects.values('condition')
        .annotate(total=Count('id'))
        .order_by('condition')
    )
    condition_labels = [item['condition'] for item in assets_by_condition]
    condition_data = [item['total'] for item in assets_by_condition]

    # --- Assets by Department (for Bar Chart) ---
    assets_by_department = (
        Asset.objects.values('department__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]  # Top 8 departments
    )
    department_labels = [item['department__name'] or "Unassigned" for item in assets_by_department]
    department_data = [item['total'] for item in assets_by_department]

    # --- Assets by Category (for Horizontal Bar Chart) ---
    assets_by_category = (
        Asset.objects.values('category__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:6]  # Top 6 categories
    )
    category_labels = [item['category__name'] or "Uncategorized" for item in assets_by_category]
    category_data = [item['total'] for item in assets_by_category]

    # --- Recent Asset Movements (Last 30 days) ---
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_movements = AssetMovement.objects.filter(
        date_moved__gte=thirty_days_ago
    ).count()

    # --- Maintenance Statistics ---
    total_maintenance_records = MaintenanceRecord.objects.count()
    recent_maintenance = MaintenanceRecord.objects.filter(
        maintenance_date__gte=thirty_days_ago.date()
    ).count()
    
    # --- Top Departments by Asset Count ---
    top_departments = (
        Department.objects.annotate(asset_count=Count('asset'))
        .order_by('-asset_count')[:5]
    )

    # --- Recent Assets Added (Last 10) ---
    recent_assets = Asset.objects.select_related(
        'department', 'category', 'assigned_to'
    ).order_by('-date_added')[:10]

    # --- Assets Needing Attention ---
    assets_needing_attention = Asset.objects.filter(
        Q(status="Under Maintenance") | Q(condition="Poor")
    ).select_related('department', 'category')[:8]

    # --- Monthly Asset Addition Trend (Last 6 months) ---
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_additions = []
    month_labels = []
    
    for i in range(5, -1, -1):
        month_start = timezone.now() - timedelta(days=i*30)
        month_end = timezone.now() - timedelta(days=(i-1)*30) if i > 0 else timezone.now()
        
        count = Asset.objects.filter(
            date_added__gte=month_start,
            date_added__lt=month_end
        ).count()
        
        monthly_additions.append(count)
        month_labels.append(month_start.strftime('%b %Y'))

    # --- Assets Distribution by Status and Department (for Stacked Bar) ---
    dept_status_data = {}
    for dept in Department.objects.all()[:6]:  # Top 6 departments
        dept_status_data[dept.name] = {
            'Available': Asset.objects.filter(department=dept, status='Available').count(),
            'In Use': Asset.objects.filter(department=dept, status='In Use').count(),
            'Under Maintenance': Asset.objects.filter(department=dept, status='Under Maintenance').count(),
        }

    # --- Context ---
    context = {
        # Basic Stats
        'total_assets': total_assets,
        'assets_in_use': assets_in_use,
        'assets_available': assets_available,
        'assets_under_maintenance': assets_under_maintenance,
        'assets_disposed': assets_disposed,
        'department_count': department_count,
        'category_count': category_count,
        'recent_movements': recent_movements,
        'total_maintenance_records': total_maintenance_records,
        'recent_maintenance': recent_maintenance,
        
        # Percentages
        'in_use_percentage': in_use_percentage,
        'maintenance_percentage': maintenance_percentage,
        'available_percentage': available_percentage,
        
        # Chart Data - Status
        'status_labels': status_labels,
        'status_data': status_data,
        
        # Chart Data - Condition
        'condition_labels': condition_labels,
        'condition_data': condition_data,
        
        # Chart Data - Department
        'department_labels': department_labels,
        'department_data': department_data,
        
        # Chart Data - Category
        'category_labels': category_labels,
        'category_data': category_data,
        
        # Chart Data - Monthly Trend
        'month_labels': month_labels,
        'monthly_additions': monthly_additions,
        
        # Department Status Distribution
        'dept_status_data': dept_status_data,
        
        # Tables
        'top_departments': top_departments,
        'recent_assets': recent_assets,
        'assets_needing_attention': assets_needing_attention,
    }

    return render(request, 'assets/dashboard.html', context)

# -------------------------------
# Asset CRUD Operations
# -------------------------------
@login_required
def asset_list(request):
    assets = Asset.objects.select_related('department', 'category').order_by('-date_added')
    return render(request, 'assets/asset_list.html', {'assets': assets})


@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset added successfully!")
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Add Asset'})


@login_required
def edit_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset updated successfully!")
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Edit Asset'})


@login_required
def delete_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    asset.delete()
    messages.warning(request, "Asset deleted successfully!")
    return redirect('asset_list')


@login_required
def asset_detail(request, id):
    asset = get_object_or_404(Asset, id=id)
    maintenance = MaintenanceRecord.objects.filter(asset=asset)
    movements = AssetMovement.objects.filter(asset=asset)
    context = {'asset': asset, 'maintenance': maintenance, 'movements': movements}
    return render(request, 'assets/asset_detail.html', context)

@login_required
def checkout_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if asset.status == 'In Use':
        messages.error(request, f"{asset.name} is currently in use by another user.")
        return redirect('asset_list')

    asset.status = 'In Use'
    asset.current_user = request.user.username
    asset.last_checked_out = timezone.now()
    asset.save()
    messages.success(request, f"You have successfully checked out {asset.name}.")
    return redirect('asset_list')

@login_required
def return_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.status = 'Available'
    asset.current_user = None
    asset.expected_return_time = None
    asset.save()
    messages.success(request, f"{asset.name} has been returned and is now available.")
    return redirect('asset_list')


# -------------------------------
# Asset Movement Views
# -------------------------------
@login_required
def movement_list(request):
    movements = AssetMovement.objects.select_related('asset', 'from_department', 'to_department').order_by('-date_moved')
    return render(request, 'assets/movement_list.html', {'movements': movements})


@login_required
def add_movement(request):
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.moved_by = request.user
            movement.save()
            messages.success(request, "Asset movement recorded successfully!")
            return redirect('movement_list')
    else:
        form = MovementForm()
    return render(request, 'assets/movement_form.html', {'form': form, 'title': 'Record Movement'})

@login_required
def edit_movement(request, id):
    movement = get_object_or_404(AssetMovement, id=id)
    
    if request.method == 'POST':
        form = MovementForm(request.POST, instance=movement)
        if form.is_valid():
            form.save()
            messages.success(request, "Movement record updated successfully.")
            return redirect('movement_list')
    else:
        form = MovementForm(instance=movement)
    
    return render(request, 'assets/movement_form.html', {
        'form': form,
        'title': 'Edit Movement'
    })

@login_required
def delete_movement(request, id):
    movement = get_object_or_404(AssetMovement, id=id)

    if request.method == "POST":
        movement.delete()
        messages.success(request, "Movement record deleted successfully.")
        return redirect('movement_list')

    return render(request, 'assets/confirm_delete.html', {
        'object': movement,
        'type': 'Movement Record'
    })


# -------------------------------
# Maintenance Views
# -------------------------------
@login_required
def maintenance_list(request):
    maintenance_records = MaintenanceRecord.objects.select_related('asset').order_by('-maintenance_date')
    return render(request, 'assets/maintenance_list.html', {'records': maintenance_records})


@login_required
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance record added successfully!")
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'assets/maintenance_form.html', {'form': form, 'title': 'Add Maintenance Record'})

@login_required
def edit_maintenance(request, id):
    record = get_object_or_404(MaintenanceRecord, id=id)
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance record updated successfully.")
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm(instance=record)

    return render(request, 'assets/maintenance_form.html', {
        'form': form,
        'title': 'Edit Maintenance Record'
    })


@login_required
def delete_maintenance(request, id):
    record = get_object_or_404(MaintenanceRecord, id=id)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Maintenance record deleted successfully.")
        return redirect('maintenance_list')

    return render(request, 'assets/confirm_delete.html', {
        'object': record,
        'type': 'Maintenance Record'
    })


# -------------------------------
# Reports View
# -------------------------------

@login_required
def reports(request):
    total_assets = Asset.objects.count()
    maintenance_count = MaintenanceRecord.objects.count()
    movement_count = AssetMovement.objects.count()

    assets_by_category = (
        Asset.objects.values('category__name')
        .annotate(count=Count('id'))
        .order_by('category__name')
    )
    assets_by_department = (
        Asset.objects.values('department__name')
        .annotate(count=Count('id'))
        .order_by('department__name')
    )

    context = {
        'total_assets': total_assets,
        'maintenance_count': maintenance_count,
        'movement_count': movement_count,
        'assets_by_category': assets_by_category,
        'assets_by_department': assets_by_department,
    }
    return render(request, 'assets/reports.html', context)
