install.packages("ggspatial", repos='http://cran.us.r-project.org')
library(devtools)
devtools::install_github("terencebarrett/USGSlidar", ref = "setup_redhat", build_vignettes = TRUE)