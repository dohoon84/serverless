class ResultForm:
  def __init__(self):
    self.__data = '';
    self.__status = True;

  @property
  def data(self, data):
    return self.__data;

  @data.setter
  def data(self, data):
    self.__data = data;

  @property
  def status(self):
    return self.__status;

  @status.setter
  def status(self, status):
    self.__status = status;

  def serialize(self):
    return {
      'data' : self.__data,
      'status': self.__status
    }