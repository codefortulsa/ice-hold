
from inmates import save, city

save.save_csv('data/tulsa_city_inmates.csv', city.inmate_generator())
