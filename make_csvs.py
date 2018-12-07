
from inmates import save, city, county

save.save_csv('data/tulsa_city_inmates.csv', city.inmate_generator())
save.save_csv('data/dlm_inmates.csv', county.inmate_generator())
