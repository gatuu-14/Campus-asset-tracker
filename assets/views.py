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
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'assets/login.html')


# -------------------------------
# Logout View
# -------------------------------
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# -------------------------------
# Home View
# -------------------------------
@login_required
def home(request):
    total_assets = Asset.objects.count()
    assets_in_use = Asset.objects.filter(status='In Use').count()
    assets_under_maintenance = Asset.objects.filter(status='Under Maintenance').count()
    department_count = Department.objects.count()
    recent_movements = AssetMovement.objects.select_related('asset', 'from_department', 'to_department').order_by('-date_moved')[:5]

    context = {
        'user': request.user,
        'total_assets': total_assets,
        'assets_in_use': assets_in_use,
        'assets_under_maintenance': assets_under_maintenance,
        'department_count': department_count,
        'recent_movements': recent_movements,
    }
    return render(request, 'assets/home.html', context)


# -------------------------------
# Dashboard View
# -------------------------------
@login_required
def dashboard(request):
    # --- Basic Counts ---
    total_assets = Asset.objects.count()
    assets_in_use = Asset.objects.filter(status="In Use").count()
    assets_under_maintenance = Asset.objects.filter(status="Under Maintenance").count()
    department_count = Department.objects.count()

    # --- Assets by Condition ---
    assets_by_condition = (
        Asset.objects.values('condition')
        .annotate(total=Count('id'))
        .order_by('condition')
    )
    condition_labels = [item['condition'] for item in assets_by_condition]
    condition_data = [item['total'] for item in assets_by_condition]

    # --- Assets by Department ---
    assets_by_department = (
        Asset.objects.values('department__name')
        .annotate(total=Count('id'))
        .order_by('department__name')
    )
    department_labels = [item['department__name'] or "Unassigned" for item in assets_by_department]
    department_data = [item['total'] for item in assets_by_department]

    # --- Context ---
    context = {
        'total_assets': total_assets,
        'assets_in_use': assets_in_use,
        'assets_under_maintenance': assets_under_maintenance,
        'department_count': department_count,
        'condition_labels': condition_labels,
        'condition_data': condition_data,
        'department_labels': department_labels,
        'department_data': department_data,
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
