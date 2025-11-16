from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from assets.models import Department, AssetCategory, Asset, AssetMovement, MaintenanceRecord
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed database with Murang\'a University sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data for Murang\'a University...')

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        MaintenanceRecord.objects.all().delete()
        AssetMovement.objects.all().delete()
        Asset.objects.all().delete()
        AssetCategory.objects.all().delete()
        Department.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create Users
        self.stdout.write('Creating users...')
        users = {
            'admin': User.objects.create_superuser('admin', 'admin@mut.ac.ke', 'admin123'),
            'john_kamau': User.objects.create_user('jkamau', 'j.kamau@mut.ac.ke', 'password123', 
                                                    first_name='John', last_name='Kamau'),
            'grace_wanjiru': User.objects.create_user('gwanjiru', 'g.wanjiru@mut.ac.ke', 'password123',
                                                       first_name='Grace', last_name='Wanjiru'),
            'peter_mwangi': User.objects.create_user('pmwangi', 'p.mwangi@mut.ac.ke', 'password123',
                                                      first_name='Peter', last_name='Mwangi'),
            'mary_njeri': User.objects.create_user('mnjeri', 'm.njeri@mut.ac.ke', 'password123',
                                                    first_name='Mary', last_name='Njeri'),
            'david_ochieng': User.objects.create_user('dochieng', 'd.ochieng@mut.ac.ke', 'password123',
                                                       first_name='David', last_name='Ochieng'),
        }
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Create Departments
        self.stdout.write('Creating departments...')
        departments = {
            'cs': Department.objects.create(
                name='Computer Science',
                location='Main Campus - Building A',
                head_of_department='Dr. James Kariuki'
            ),
            'it': Department.objects.create(
                name='Information Technology',
                location='Main Campus - Building B',
                head_of_department='Dr. Ann Wambui'
            ),
            'business': Department.objects.create(
                name='Business Administration',
                location='Main Campus - Building C',
                head_of_department='Dr. Samuel Njoroge'
            ),
            'engineering': Department.objects.create(
                name='Engineering',
                location='Main Campus - Building D',
                head_of_department='Dr. Patricia Akinyi'
            ),
            'library': Department.objects.create(
                name='University Library',
                location='Central Library Building',
                head_of_department='Mr. Francis Gitau'
            ),
            'ict': Department.objects.create(
                name='ICT Services',
                location='ICT Center',
                head_of_department='Eng. Michael Waweru'
            ),
            'admin': Department.objects.create(
                name='Administration',
                location='Administration Block',
                head_of_department='Mrs. Lucy Muthoni'
            ),
        }
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments'))

        # Create Asset Categories
        self.stdout.write('Creating asset categories...')
        categories = {
            'computers': AssetCategory.objects.create(
                name='Computers & Laptops',
                description='Desktop computers, laptops, and workstations'
            ),
            'networking': AssetCategory.objects.create(
                name='Networking Equipment',
                description='Routers, switches, access points, and network cables'
            ),
            'printers': AssetCategory.objects.create(
                name='Printers & Scanners',
                description='Printers, scanners, and multifunction devices'
            ),
            'projectors': AssetCategory.objects.create(
                name='Projectors & Displays',
                description='Projectors, smart boards, and display screens'
            ),
            'furniture': AssetCategory.objects.create(
                name='Office Furniture',
                description='Desks, chairs, cabinets, and shelving'
            ),
            'lab_equipment': AssetCategory.objects.create(
                name='Laboratory Equipment',
                description='Lab tools, testing equipment, and specialized devices'
            ),
            'vehicles': AssetCategory.objects.create(
                name='Vehicles',
                description='University vehicles and transportation'
            ),
            'servers': AssetCategory.objects.create(
                name='Servers & Storage',
                description='Server hardware and storage devices'
            ),
        }
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} asset categories'))

        # Create Assets
        self.stdout.write('Creating assets...')
        assets_data = [
            # Computers
            {
                'name': 'Dell OptiPlex 7090',
                'category': categories['computers'],
                'serial_number': 'MUT-CS-001',
                'department': departments['cs'],
                'assigned_to': users['john_kamau'],
                'purchase_date': datetime(2023, 3, 15).date(),
                'condition': 'Good',
                'status': 'In Use',
                'description': 'Desktop computer for CS Lab 1',
                'current_user': 'John Kamau'
            },
            {
                'name': 'HP EliteBook 840',
                'category': categories['computers'],
                'serial_number': 'MUT-IT-002',
                'department': departments['it'],
                'assigned_to': users['grace_wanjiru'],
                'purchase_date': datetime(2023, 6, 20).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Laptop for IT staff',
                'current_user': 'Grace Wanjiru'
            },
            {
                'name': 'Lenovo ThinkCentre M720',
                'category': categories['computers'],
                'serial_number': 'MUT-CS-003',
                'department': departments['cs'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 1, 10).date(),
                'condition': 'Fair',
                'status': 'Under Maintenance',
                'description': 'Desktop requiring RAM upgrade'
            },
            {
                'name': 'Apple MacBook Pro 14"',
                'category': categories['computers'],
                'serial_number': 'MUT-BUS-004',
                'department': departments['business'],
                'assigned_to': users['peter_mwangi'],
                'purchase_date': datetime(2024, 2, 5).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Laptop for multimedia presentations',
                'current_user': 'Peter Mwangi'
            },
            {
                'name': 'Acer Aspire Desktop',
                'category': categories['computers'],
                'serial_number': 'MUT-LIB-005',
                'department': departments['library'],
                'assigned_to': None,
                'purchase_date': datetime(2022, 8, 12).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'Library catalog station'
            },
            
            # Networking Equipment
            {
                'name': 'Cisco Catalyst 2960 Switch',
                'category': categories['networking'],
                'serial_number': 'MUT-ICT-101',
                'department': departments['ict'],
                'assigned_to': users['david_ochieng'],
                'purchase_date': datetime(2023, 4, 18).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': '48-port managed switch for main building',
                'current_user': 'David Ochieng'
            },
            {
                'name': 'TP-Link Access Point AC1750',
                'category': categories['networking'],
                'serial_number': 'MUT-ICT-102',
                'department': departments['ict'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 7, 25).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'WiFi access point for Building A'
            },
            {
                'name': 'Ubiquiti EdgeRouter',
                'category': categories['networking'],
                'serial_number': 'MUT-ICT-103',
                'department': departments['ict'],
                'assigned_to': users['david_ochieng'],
                'purchase_date': datetime(2024, 1, 8).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Main campus router',
                'current_user': 'David Ochieng'
            },
            
            # Printers
            {
                'name': 'HP LaserJet Pro M404dn',
                'category': categories['printers'],
                'serial_number': 'MUT-ADM-201',
                'department': departments['admin'],
                'assigned_to': users['mary_njeri'],
                'purchase_date': datetime(2023, 5, 10).date(),
                'condition': 'Good',
                'status': 'In Use',
                'description': 'Administration office printer',
                'current_user': 'Mary Njeri'
            },
            {
                'name': 'Canon imageRUNNER 2625',
                'category': categories['printers'],
                'serial_number': 'MUT-CS-202',
                'department': departments['cs'],
                'assigned_to': None,
                'purchase_date': datetime(2022, 11, 30).date(),
                'condition': 'Fair',
                'status': 'Under Maintenance',
                'description': 'Multifunction printer - toner replacement needed'
            },
            {
                'name': 'Epson EcoTank L3150',
                'category': categories['printers'],
                'serial_number': 'MUT-LIB-203',
                'department': departments['library'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 9, 14).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'Library printing services'
            },
            
            # Projectors
            {
                'name': 'Epson EB-X49',
                'category': categories['projectors'],
                'serial_number': 'MUT-CS-301',
                'department': departments['cs'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 2, 20).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'Lecture hall projector - CS Lab 1'
            },
            {
                'name': 'BenQ MH535FHD',
                'category': categories['projectors'],
                'serial_number': 'MUT-BUS-302',
                'department': departments['business'],
                'assigned_to': users['peter_mwangi'],
                'purchase_date': datetime(2024, 3, 5).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Business presentation room',
                'current_user': 'Peter Mwangi'
            },
            {
                'name': 'Sony VPL-FHZ58',
                'category': categories['projectors'],
                'serial_number': 'MUT-ENG-303',
                'department': departments['engineering'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 8, 22).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'Engineering workshop projector'
            },
            
            # Servers
            {
                'name': 'Dell PowerEdge R740',
                'category': categories['servers'],
                'serial_number': 'MUT-ICT-401',
                'department': departments['ict'],
                'assigned_to': users['david_ochieng'],
                'purchase_date': datetime(2023, 10, 15).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Main database server',
                'current_user': 'David Ochieng'
            },
            {
                'name': 'HP ProLiant DL380 Gen10',
                'category': categories['servers'],
                'serial_number': 'MUT-ICT-402',
                'department': departments['ict'],
                'assigned_to': users['david_ochieng'],
                'purchase_date': datetime(2024, 1, 20).date(),
                'condition': 'Excellent',
                'status': 'In Use',
                'description': 'Web application server',
                'current_user': 'David Ochieng'
            },
            
            # Lab Equipment
            {
                'name': 'Oscilloscope Tektronix TBS2000',
                'category': categories['lab_equipment'],
                'serial_number': 'MUT-ENG-501',
                'department': departments['engineering'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 4, 12).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'Electronics lab equipment'
            },
            {
                'name': 'Soldering Station Weller WES51',
                'category': categories['lab_equipment'],
                'serial_number': 'MUT-ENG-502',
                'department': departments['engineering'],
                'assigned_to': None,
                'purchase_date': datetime(2022, 12, 8).date(),
                'condition': 'Fair',
                'status': 'Available',
                'description': 'Student lab workstation'
            },
            
            # Furniture
            {
                'name': 'Executive Desk Oak Finish',
                'category': categories['furniture'],
                'serial_number': 'MUT-ADM-601',
                'department': departments['admin'],
                'assigned_to': users['mary_njeri'],
                'purchase_date': datetime(2023, 1, 5).date(),
                'condition': 'Good',
                'status': 'In Use',
                'description': 'Administration office furniture',
                'current_user': 'Mary Njeri'
            },
            {
                'name': 'Ergonomic Office Chair',
                'category': categories['furniture'],
                'serial_number': 'MUT-CS-602',
                'department': departments['cs'],
                'assigned_to': users['john_kamau'],
                'purchase_date': datetime(2023, 6, 18).date(),
                'condition': 'Good',
                'status': 'In Use',
                'description': 'Staff office chair',
                'current_user': 'John Kamau'
            },
            
            # Vehicles
            {
                'name': 'Toyota Hilux Double Cab',
                'category': categories['vehicles'],
                'serial_number': 'MUT-VEH-701',
                'department': departments['admin'],
                'assigned_to': None,
                'purchase_date': datetime(2022, 7, 20).date(),
                'condition': 'Good',
                'status': 'Available',
                'description': 'University utility vehicle - KCB 123X'
            },
            {
                'name': 'Nissan NV350 Urvan',
                'category': categories['vehicles'],
                'serial_number': 'MUT-VEH-702',
                'department': departments['admin'],
                'assigned_to': None,
                'purchase_date': datetime(2023, 3, 15).date(),
                'condition': 'Excellent',
                'status': 'Available',
                'description': 'Student transport bus - KCD 456Y'
            },
        ]

        assets = {}
        for idx, asset_data in enumerate(assets_data):
            asset = Asset.objects.create(**asset_data)
            assets[f'asset_{idx}'] = asset

        self.stdout.write(self.style.SUCCESS(f'Created {len(assets)} assets'))

        # Create Asset Movements
        self.stdout.write('Creating asset movements...')
        movements_data = [
            {
                'asset': assets['asset_2'],  # Lenovo ThinkCentre
                'from_department': departments['cs'],
                'to_department': departments['it'],
                'moved_by': users['admin'],
                'remarks': 'Transferred for IT department use after CS lab upgrade'
            },
            {
                'asset': assets['asset_13'],  # BenQ Projector
                'from_department': departments['business'],
                'to_department': departments['cs'],
                'moved_by': users['grace_wanjiru'],
                'remarks': 'Temporarily moved for guest lecture'
            },
            {
                'asset': assets['asset_6'],  # TP-Link Access Point
                'from_department': departments['ict'],
                'to_department': departments['library'],
                'moved_by': users['david_ochieng'],
                'remarks': 'Installed to improve library WiFi coverage'
            },
        ]

        for movement_data in movements_data:
            AssetMovement.objects.create(**movement_data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(movements_data)} asset movements'))

        # Create Maintenance Records
        self.stdout.write('Creating maintenance records...')
        maintenance_data = [
            {
                'asset': assets['asset_2'],  # Lenovo ThinkCentre
                'issue_reported': 'Computer running slow, needs RAM upgrade',
                'maintenance_date': (timezone.now() - timedelta(days=5)).date(),
                'performed_by': 'ICT Technician - Michael Kamau',
                'remarks': 'RAM upgraded from 8GB to 16GB. System performance improved.'
            },
            {
                'asset': assets['asset_9'],  # Canon Printer
                'issue_reported': 'Printer showing "replace toner" error',
                'maintenance_date': (timezone.now() - timedelta(days=10)).date(),
                'performed_by': 'Canon Service Center',
                'remarks': 'Toner cartridge replaced. Print quality test passed.'
            },
            {
                'asset': assets['asset_5'],  # Cisco Switch
                'issue_reported': 'Routine firmware update required',
                'maintenance_date': (timezone.now() - timedelta(days=15)).date(),
                'performed_by': 'David Ochieng',
                'remarks': 'Firmware updated to latest version. No issues detected.'
            },
            {
                'asset': assets['asset_19'],  # Toyota Hilux
                'issue_reported': 'Scheduled service at 50,000 km',
                'maintenance_date': (timezone.now() - timedelta(days=20)).date(),
                'performed_by': 'Toyota Service Center - Murang\'a',
                'remarks': 'Oil change, filter replacement, brake inspection completed.'
            },
            {
                'asset': assets['asset_0'],  # Dell OptiPlex
                'issue_reported': 'Hard disk making clicking noise',
                'maintenance_date': (timezone.now() - timedelta(days=30)).date(),
                'performed_by': 'ICT Technician - Michael Kamau',
                'remarks': 'Hard disk replaced with SSD. Data migrated successfully.'
            },
        ]

        for maintenance in maintenance_data:
            MaintenanceRecord.objects.create(**maintenance)

        self.stdout.write(self.style.SUCCESS(f'Created {len(maintenance_data)} maintenance records'))

        self.stdout.write(self.style.SUCCESS('✓ Database seeded successfully with Murang\'a University data!'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS('  Username: admin'))
        self.stdout.write(self.style.SUCCESS('  Password: admin123'))
        self.stdout.write(self.style.SUCCESS('\nOther test users: jkamau, gwanjiru, pmwangi, mnjeri, dochieng'))
        self.stdout.write(self.style.SUCCESS('  Password for all: password123'))