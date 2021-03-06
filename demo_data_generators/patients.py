# pylint: disable=too-many-locals
# pylint: disable=R0903
"""
Generate Fake Patients based on the locations created
"""
from faker import Factory
from xml.etree.ElementTree import Element, SubElement
import random


class PatientsGenerator(object):
    """
    Generate Patients
    """

    def __init__(self, patient_id_offset, patients_in_bed, patients_out_bed,
                 ward):
        self.data_generator = Factory.create()

        # Create root element
        self.root = Element('openerp')

        # Create data inside root element
        self.data = SubElement(self.root, 'data', {'noupdate': '1'})

        # Gender / Sex list
        self.gender_sex_list = ['M', 'F']

        # Ethnicity list
        self.ethnicity_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J',
                               'K', 'L', 'M', 'N', 'P', 'R', 'S', 'Z']

        # Generate patients in bed
        self.generate_patients(patient_id_offset=patient_id_offset,
                               total_patients=patients_in_bed, ward=ward)

        # Generate patients not in bed
        non_bed_patient_offset = (patient_id_offset + patients_in_bed)
        self.generate_patients(patient_id_offset=non_bed_patient_offset,
                               total_patients=patients_out_bed, in_bed=False,
                               ward=ward)

    def generate_patients(self, patient_id_offset=0, total_patients=28,
                          in_bed=True, ward='a'):
        """
        A function to create a bunch of patients for the XML document
        :param patient_id_offset: the number to offset the IDs from
        :param total_patients: the number of patients to add to the XML doc
        :param in_bed: If the patients should be in bed or not
        :param ward: The name of the ward
        :return:
        """
        for item in xrange(0, total_patients):
            item_delta = item + 1
            patient_id = patient_id_offset + item
            # Create record with id and patient model
            record = SubElement(
                self.data,
                'record',
                {
                    'model': 'nh.clinical.patient',
                    'id': 'nhc_demo_patient_{0}'.format(patient_id)
                }
            )

            # create DOB field with fake data
            dob_field = SubElement(record, 'field', {'name': 'dob'})
            dob_field.text = '{0}'.format(
                self.data_generator.date_time_between(
                    start_date="-90y", end_date="-18y"))

            # Create Gender / Sex fields with fake data
            gender_sex = random.choice(self.gender_sex_list)
            gender_field = SubElement(record, 'field', {'name': 'gender'})
            gender_field.text = gender_sex
            sex_field = SubElement(record, 'field', {'name': 'sex'})
            sex_field.text = gender_sex

            # Create Ethnicity
            ethnicity_field = SubElement(record, 'field',
                                         {'name': 'ethnicity'})
            ethnicity_field.text = random.choice(self.ethnicity_list)

            # Create identifiers
            patient_id = str(patient_id).zfill(4)
            patient_id_field = SubElement(record, 'field',
                                          {'name': 'patient_identifier'})
            patient_id_field.text = 'NHSNUM{0}'.format(patient_id)
            other_id_field = SubElement(record, 'field',
                                        {'name': 'other_identifier'})
            other_id_field.text = 'HOSNUM{0}'.format(patient_id)

            # Create First Name
            if gender_sex == 'M':
                first_name = self.data_generator.first_name_male()
            else:
                first_name = self.data_generator.first_name_female()
            first_name_field = SubElement(record, 'field',
                                          {'name': 'given_name'})
            first_name_field.text = first_name

            # Create Middle Name
            if gender_sex == 'M':
                middle_name = self.data_generator.first_name_male()
            else:
                middle_name = self.data_generator.first_name_female()
            middle_name_field = SubElement(record, 'field',
                                           {'name': 'middle_names'})
            middle_name_field.text = middle_name

            # Create last name
            last_name = self.data_generator.last_name()
            last_name_field = SubElement(record, 'field',
                                         {'name': 'family_name'})
            last_name_field.text = last_name

            # Create location id
            bed_string = ''
            if in_bed:
                bed_string = '_b{0}'.format(item_delta)
            SubElement(
                record,
                'field',
                {
                    'name': 'current_location_id',
                    'ref': 'nhc_def_conf_location_w{0}{1}'.format(ward,
                                                                  bed_string)
                }
            )
