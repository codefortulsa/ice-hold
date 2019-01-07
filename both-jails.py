import multiprocessing

from inmates import save, city, county

def cty():
    save.save_csv('data/tulsa_city_inmates.csv', city.inmate_generator())

def dlm():
    save.save_csv('data/dlm_inmates.csv', county.inmate_generator())

if __name__ == '__main__':
    p1 = multiprocessing.Process(name='city jail', target=cty)
    p = multiprocessing.Process(name='dl moss', target=dlm)
    p1.start()
    p.start()
