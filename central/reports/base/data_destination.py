import abc

from django.http import HttpResponse


class BaseDataDestination(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_destination_object(self):
        pass

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def write(self, content):
        pass


class HTTPResponseDataDestination(BaseDataDestination):

    def __init__(self, filename):
        self.__response = HttpResponse(content_type='text/csv')
        self.__response['Content-Disposition'] = f'attachment; filename="{filename}"'

    def write(self, content):
        self.__response.write(content)

    def get_destination_object(self, *args, **kwargs):
        return self.__response

    def save(self):
        return self.__response
