# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo, DataRequired, IPAddress
from wtforms import ValidationError
from ..models import User, Department, Idc, Software, Project, Module, Environment


class AddProjectForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    department = SelectField('Department', coerce=int)
    pm = SelectField('ProjectManager', coerce=int)
    sla = SelectField('SLA', coerce=str)
    check_point = StringField('CheckPoint')
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.pm.choices = [(0, 'Choose...')] + [(pm.id, pm.username)
                             for pm in User.query.order_by(User.username).all()]
        self.department.choices = [(0, 'Choose...')] + [(department.id, department.name)
                                   for department in Department.query.order_by(Department.name).all()]
        self.sla.choices = [(i, i) for i in current_app.config['SLA']]

    @staticmethod
    def validate_name(self, field):
        if Project.query.filter_by(name=field.data).first():
            raise ValidationError('ProjectName already in use.')


class EditProjectForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_department = SelectField('Department', coerce=int)
    e_pm = SelectField('ProjectManager', coerce=int)
    e_sla = SelectField('SLA', coerce=str)
    e_check_point = StringField('CheckPoint')
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.e_pm.choices = [(pm.id, pm.username)
                             for pm in User.query.order_by(User.username).all()]
        self.e_department.choices = [(department.id, department.name)
                                   for department in Department.query.order_by(Department.name).all()]
        self.e_sla.choices = [(i, i) for i in current_app.config['SLA']]

    @staticmethod
    def validate_name(self, field):
        if Project.query.filter_by(name=field.data).first():
            raise ValidationError('ProjectName already in use.')


class AddModuleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    project = SelectField('Project', coerce=int, validators=[InputRequired()])
    svn = StringField('SVN')
    parent = SelectField('PerModule', coerce=int, default=0)
    dev = SelectField('DEV', coerce=int)
    qa = SelectField('QA', coerce=int)
    ops = SelectField('OPS', coerce=int)
    software = SelectField('SOFTWARE', coerce=int)
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddModuleForm, self).__init__(*args, **kwargs)
        self.project.choices = [(0, 'Choose...')] + [(project.id, project.name)
                            for project in Project.query.order_by(Project.name).all()]
        self.parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                            for parent in Module.query.order_by(Module.name).all()]
        self.dev.choices = [(0, 'None')] + [(dev.id, dev.username)
                            for dev in User.query.filter_by(type="dev").order_by(User.username).all()]
        self.qa.choices = [(0, 'None')] + [(qa.id, qa.username)
                            for qa in User.query.filter_by(type="qa").order_by(User.username).all()]
        self.ops.choices = [(0, 'None')] + [(ops.id, ops.username)
                            for ops in User.query.filter_by(type="ops").order_by(User.username).all()]
        self.software.choices = [(0, 'Choose...')] + [(software.id, software.version)
                            for software in Software.query.order_by(Software.version).all()]

    @staticmethod
    def validate_name(self, field):
        if Module.query.filter_by(name=field.data).first():
            raise ValidationError('ModuleName already in use.')


class EditModuleForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_project = SelectField('Project', coerce=int, validators=[InputRequired()])
    e_svn = StringField('SVN')
    e_parent = SelectField('PerModule', coerce=int)
    e_dev = SelectField('DEV', coerce=int)
    e_qa = SelectField('QA', coerce=int)
    e_ops = SelectField('OPS', coerce=int)
    e_software = SelectField('SOFTWARE', coerce=int)
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditModuleForm, self).__init__(*args, **kwargs)
        self.e_project.choices = [(project.id, project.name)
                                for project in Project.query.order_by(Project.name).all()]
        self.e_parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                               for parent in Module.query.order_by(Module.name).all()]
        self.e_dev.choices = [(0, 'None')] + [(dev.id, dev.username)
                            for dev in User.query.filter_by(type="dev").order_by(User.username).all()]
        self.e_qa.choices = [(0, 'None')] + [(qa.id, qa.username)
                           for qa in User.query.filter_by(type="qa").order_by(User.username).all()]
        self.e_ops.choices = [(0, 'None')] + [(ops.id, ops.username)
                            for ops in User.query.filter_by(type="ops").order_by(User.username).all()]
        self.e_software.choices = [(software.id, software.version)
                                 for software in Software.query.order_by(Software.version).all()]

    @staticmethod
    def validate_name(self, field):
        if Module.query.filter_by(name=field.data).first():
            raise ValidationError('ModuleName already in use.')


class AddEnvironmentForm(FlaskForm):
    module = SelectField('Module', coerce=int, validators=[InputRequired()])
    idc = SelectField('IDC', coerce=int)
    env = SelectField('ENV', coerce=str)
    check_point1 = StringField('Check_Point1')
    check_point2 = StringField('Check_Point2')
    check_point3 = StringField('Check_Point3')
    deploy_path = StringField('deploy_path')
    server_ip = StringField('server_ip')
    online_since = DateTimeField('Start at', format="%Y-%m-%d %H:%M:%S")
    domain = StringField('Domain')

    def __init__(self, *args, **kwargs):
        super(AddEnvironmentForm, self).__init__(*args, **kwargs)
        self.module.choices = [(0, 'Choose...')] + [(module.id, module.name)
                            for module in Module.query.order_by(Module.name).all()]
        self.idc.choices = [(0, 'Choose...')] + [(idc.id, idc.name)
                                   for idc in Idc.query.order_by(Idc.name).all()]
        self.env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]

    @staticmethod
    def validate_name(self, field):
        if Environment.query.filter_by(name=field.data).first():
            raise ValidationError('Environment already in use.')


class EditEnvironmentForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_module = SelectField('Module', coerce=int, validators=[InputRequired()])
    e_idc = SelectField('IDC', coerce=int)
    e_env = SelectField('ENV', coerce=str)
    e_check_point1 = StringField('Check_Point1')
    e_check_point2 = StringField('Check_Point2')
    e_check_point3 = StringField('Check_Point3')
    e_deploy_path = StringField('deploy_path')
    e_server_ip = StringField('server_ip')
    e_online_since = DateTimeField('Start at', format="%Y-%m-%d %H:%M:%S")
    e_domain = StringField('Domain')

    def __init__(self, *args, **kwargs):
        super(EditEnvironmentForm, self).__init__(*args, **kwargs)
        self.e_module.choices = [(module.id, module.name)
                            for module in Module.query.order_by(Module.name).all()]
        self.e_idc.choices = [(idc.id, idc.name)
                            for idc in Idc.query.order_by(Idc.name).all()]
        self.e_env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]

    @staticmethod
    def validate_name(self, field):
        if Environment.query.filter_by(name=field.data).first():
            raise ValidationError('Environment already in use.')