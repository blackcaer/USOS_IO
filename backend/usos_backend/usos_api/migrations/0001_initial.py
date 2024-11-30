# Generated by Django 5.1.3 on 2024-11-30 20:45

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryAttendanceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryGradeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryStudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryUserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsentTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('is_mandatory', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(default='name_example', max_length=255)),
                ('first_name', models.CharField(default='name_example', max_length=255)),
                ('middle_name', models.CharField(blank=True, default='Mname_example', max_length=255, null=True)),
                ('last_name', models.CharField(default='Lname_example', max_length=255)),
                ('email', models.EmailField(default='example@example.com', max_length=254, unique=True)),
                ('birth_date', models.DateField(default='2010-01-01')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=15)),
                ('status', models.CharField(choices=[('A', 'Active'), ('D', 'Unactive')], default='A', max_length=31)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('photo_url', models.URLField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence_reason', models.TextField(null=True)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usos_api.categoryattendancestatus')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='school_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.schoolsubject'),
        ),
        migrations.CreateModel(
            name='GradeColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('default_weight', models.IntegerField()),
                ('school_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.schoolsubject')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parents', models.ManyToManyField(related_name='children', to='usos_api.parent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParentConsent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_consent', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('consent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.consenttemplate')),
                ('parent_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.parent')),
                ('child_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.student')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('count_to_avg', models.BooleanField(default=True)),
                ('value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usos_api.categorygradevalue')),
                ('grade_column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.gradecolumn')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('level', models.IntegerField()),
                ('section', models.CharField(blank=True, max_length=50, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usos_api.categorystudentgroup')),
                ('students', models.ManyToManyField(related_name='student_groups', to='usos_api.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='groups',
            field=models.ManyToManyField(to='usos_api.studentgroup'),
        ),
        migrations.AddField(
            model_name='schoolsubject',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.studentgroup'),
        ),
        migrations.AddField(
            model_name='consenttemplate',
            name='recipients',
            field=models.ManyToManyField(to='usos_api.studentgroup'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.ManyToManyField(blank=True, to='usos_api.studentgroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('school_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.schoolsubject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.teacher'),
        ),
        migrations.AddField(
            model_name='consenttemplate',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usos_api.teacher'),
        ),
    ]
