import primary_key_discovery as pk
import foreign_key_discovery as fk

# import get_files as gf
# dat_path, dat_source, sample_data, files = gf.get_files('kaggle', 'av_healthcare')


#-------------------------
# primary key tests
#-------------------------

# av health care
av_health_pk = pk.find_primary_keys('kaggle', 'av_healthcare')

# flight data
flights_pk = pk.find_primary_keys('kaggle', 'flights')

# bristish prescriptions
british_prescrip_pk = pk.find_primary_keys('kaggle', 'british_prescribing')

# imdb movies
imdb_pk = pk.find_primary_keys('kaggle', 'imdb_movies')


#--------------------
# foreign key tests
#--------------------

# av health care
# dat_path, dat_source, sample_data, files = gf.get_files('kaggle', 'av_healthcare')
av_health_fk = fk.find_foreign_keys('kaggle', 'av_healthcare')

# flight data
flights_fk = fk.find_foreign_keys('kaggle', 'flights')

# bristish prescriptions
british_prescrip_fk = fk.find_foreign_keys('kaggle', 'british_prescribing')

# imdb movies
imdb_fk = fk.find_foreign_keys('kaggle', 'imdb_movies')

#----------------------------
# foreign key code profiling
#----------------------------

from line_profiler import LineProfiler

lp = LineProfiler()
lp_wrapper = lp(fk.find_foreign_keys)
lp_wrapper('kaggle', 'av_healthcare')
lp.print_stats()
