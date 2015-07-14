import operator
import datetime
from ..models import ReportsCacheModel
import ast
from .clientservice_gets import GetAllClients
from dateutil.relativedelta import relativedelta


class ClientsReport:
  clients_by_age_group = None
  all_clients_by_sex = None
  all_clients_by_gp = None

  def __init__(self, clients=None, current=True):
    self.SudsResult = clients
    self.current = current
    self.TodayDate = datetime.datetime.today()

  def GetSudsResults(self):
    index = 1
    tpc = 0
    result = GetAllClients()
    self.SudsResult = [result.Clients.Client]
    tpc = result.TotalPageCount

    while index < tpc:
      print(index, tpc)
      index += 1
      self.SudsResult.append(GetAllClients(page=index).Clients.Client)


  def print_clients(self):
    for sale in self.SudsResult:
      print(sale)


  def all_clients_by_age(self):
    name = 'clients_by_age'
    if not self.current:
      name += '_nc'
    ages = {}
    try:
      clients_by_age = ReportsCacheModel.objects.get(datapull_datestamp=self.TodayDate, chart_name=name)
      return eval(clients_by_age.data_string)

    except ReportsCacheModel.DoesNotExist:
      if self.SudsResult == None:
        self.GetSudsResults()

      for thing in self.SudsResult:
        for client in thing:
          age = 0
          if client.BirthDate != None:
            birthday = client.BirthDate
            age = relativedelta(self.TodayDate, birthday).years

            if age != 0:
              if age <= 20:
                if "-20" in ages:
                  ages['-20'] += 1
                else:
                  ages['-20'] = 1

              if age > 20 and age <= 25:
                if "21-25" in ages:
                  ages['21-25'] += 1
                else:
                  ages['21-25'] = 1

              if age > 25 and age <= 30:
                if "26-30" in ages:
                  ages['26-30'] += 1
                else:
                  ages['26-30'] = 1

              if age > 30 and age <= 35:
                if "31-35" in ages:
                  ages['31-35'] += 1
                else:
                  ages['31-35'] = 1

              if age > 35 and age <= 40:
                if "36-40" in ages:
                  ages['36-40'] += 1
                else:
                  ages['36-40'] = 1

              if age > 40 and age <= 45:
                if "41-45" in ages:
                  ages['41-45'] += 1
                else:
                  ages['41-45'] = 1

              if age > 45 and age <= 50:
                if "46-50" in ages:
                  ages['46-50'] += 1
                else:
                  ages['46-50'] = 1

              if age > 50 and age <= 55:
                if "51-55" in ages:
                  ages['51-55'] += 1
                else:
                  ages['51-55'] = 1

              if age > 55 and age <= 60:
                if "56-60" in ages:
                  ages['56-60'] += 1
                else:
                  ages['56-60'] = 1

              if age > 60 and age <= 65:
                if "61-65" in ages:
                  ages['61-65'] += 1
                else:
                  ages['61-65'] = 1

              if age > 65:
                if "65+" in ages:
                  ages['65+'] += 1
                else:
                  ages['65+'] = 1

      clients_by_age_group = ages
      ages_by_group = sorted(clients_by_age_group.items(), key=operator.itemgetter(0))

      report = ReportsCacheModel()
      report.chart_name = name
      report.data_string = str(ages_by_group)
      report.save()

      return ages_by_group


  def client_sex(self):
      name = 'clients_by_sex'
      if not self.current:
        name += '_nc'
      sexes = {}
      try:
        all_clients_by_sex = ReportsCacheModel.objects.get(datapull_datestamp=self.TodayDate, chart_name=name)
        return eval(all_clients_by_sex.data_string)

      except ReportsCacheModel.DoesNotExist:
        if self.SudsResult == None:
          self.GetSudsResults()
          
        for thing in self.SudsResult:
          for client in thing:
            if hasattr(client, 'Gender') and client.Gender != None:
              gender = client.Gender

              if gender == 'Male':
                if "Male" in sexes:
                  sexes['Male'] += 1
                else:
                  sexes['Male'] = 1

              elif gender == 'Female':
                if "Female" in sexes:
                  sexes['Female'] += 1
                else:
                  sexes['Female'] = 1

              else:
                if "Other" in sexes:
                  sexes['Other'] += 1
                else:
                  sexes['Other'] = 1


        clients_by_sex = sexes
        all_clients_by_sex = sorted(clients_by_sex.items(), key=operator.itemgetter(0))

        report = ReportsCacheModel()
        report.chart_name = name
        report.data_string = str(all_clients_by_sex)
        report.save()

        return all_clients_by_sex


  def client_gender_pref(self):
      name = 'clients_by_gender_pref'
      if not self.current:
        name += '_nc'
      sexes = {}
      try:
        all_clients_by_gp = ReportsCacheModel.objects.get(datapull_datestamp=self.TodayDate, chart_name=name)
        return eval(all_clients_by_gp.data_string)

      except ReportsCacheModel.DoesNotExist:
        if self.SudsResult == None:
          self.GetSudsResults()
        for thing in self.SudsResult:
          for client in thing:
            if client.AppointmentGenderPreference != None:
              gender = client.AppointmentGenderPreference

              if gender == 'Male':
                if "Male" in sexes:
                  sexes['Male'] += 1
                else:
                  sexes['Male'] = 1

              elif gender == 'Female':
                if "Female" in sexes:
                  sexes['Female'] += 1
                else:
                  sexes['Female'] = 1

              else:
                if "None" in sexes:
                  sexes['None'] += 1
                else:
                  sexes['None'] = 1


        clients_by_gp = sexes
        all_clients_by_gp = sorted(clients_by_gp.items(), key=operator.itemgetter(0))

        report = ReportsCacheModel()
        report.chart_name = name
        report.data_string = str(all_clients_by_gp)
        report.save()

        return all_clients_by_gp