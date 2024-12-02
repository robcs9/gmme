import unittest
import geoservices as ctc
import plot
import re

        
class CepToCoordsTests(unittest.TestCase):
    
    def test_coordinates_retrieval(self):
        # self.assertEqual(ctc.getCoordsFromCep('50810000'), {'lat': '1', 'lng': '2'})
        pass
    def test_batch_geocode(self):
        # res = ctc.batchGeocode(['54330-075','54000-000','55000-000'])
        # aprint(res)
        pass

class PlottingTests(unittest.TestCase):
    
    def test_saving_plot(self):
        plot.plotMap()
        err_str = None
        try:
            with open('./plot.json') as fd:
                # print('plot.json found successfully')
                pass
        except Exception as e:
            print(f'Actual Exception: {e.strerror}')
            err_str = e.strerror
        self.assertEqual(err_str, None,'plot.json not found')