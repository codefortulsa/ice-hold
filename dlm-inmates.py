
from inmates import save, county

save.save_csv('data/dlm_inmates.csv', county.inmate_generator())
