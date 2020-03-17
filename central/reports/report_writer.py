from central.reports.base.data_destination import HTTPResponseDataDestination
from central.reports.base.data_writer import BaseCSVDataWriter


class CSVCommonReportResponseWriter(BaseCSVDataWriter):

    header = ',,Осенний семестр,,,,,,,,,,,Весенний семестр,,,,,,,,,,,,,,\r\n' \
             'Имя,Фамилия,Лекции,Лабораторные,Практические,Курсовые работы,Консультации,Зачеты,Экзамены,Магистратура,' \
             'Рецензирование,Другие,Итого за семестр,Лекции,Лабораторные,Практические,Курсовые работы,Консультации,' \
             'Зачеты,Экзамены,Магистратура,Дипломное проектирование,Гос экзамен,' \
             'ГЭК по защите диплома,Производственная практика,Рецензирование,Другие,Итого за семестр,Итого за год\r\n'
    format_line = '{teacher__name},{teacher__surname},{lecture_sum_0},{lab_sum_0},' \
                  '{practice_lessons_sum_0},{course_works_sum_0},{consultation_sum_0},{credit_sum_0},' \
                  '{exam_sum_0},{magistracy_sum_0},{review_sum_0},{other_sum_0},,{lecture_sum_1},' \
                  '{lab_sum_1},{practice_lessons_sum_1},{course_works_sum_1},{consultation_sum_1},{credit_sum_1},' \
                  '{exam_sum_1},{magistracy_sum_1},{diploma_sum},{gov_exam_sum},' \
                  '{gec_diploma_sum},{practice_sum},{review_sum_1},{other_sum_1},,\r\n'
    destination_class = HTTPResponseDataDestination
