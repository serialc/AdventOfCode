# Created by Aurélien Ginolhac


library(tidyverse)
library(tictoc)
library(sp)
library(sf)
options(scipen = 999)


#### Part 1
input <- "7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"


input <- "input"

parse_coord <- function(r) {
  str_split_1(r, ',') |> as.numeric()
}

compute_area <- function(a, b) {
  (abs(a[1] - b[1]) + 1) * (abs(a[2] - b[2]) + 1)
}

tic()
combn(read_lines(input), 2, simplify = FALSE) |> 
  map(\(x) list(parse_coord(x[1]), parse_coord(x[2]))) |> 
  enframe() |> 
  mutate(c1 = map(value, 1),
         c2 = map(value, 2)) -> rectangles
mutate(rectangles, area = map2_dbl(c1, c2, compute_area)) |> 
  slice_max(area, n = 1)
toc()

#### Part 2

# retrieve the data from input
tibble(coord = read_lines(input)) |> 
  mutate(cc = map(coord, parse_coord)) |> 
  unnest_wider(col = cc, names_sep = "_") |> 
  rename(x = cc_1, y = cc_2) -> red_tiles

# transform into one big shape
select(red_tiles, x, y) |> 
  as.matrix() -> gpoly
# need to close the polygon (repeat the first row)
green_area <- st_polygon(list(rbind(gpoly, gpoly[1,])), dim = "XY")

# calculate the area of every possible rectangle and sort in descending order
mutate(rectangles, area = map2_dbl(c1, c2, compute_area)) |> 
  arrange(desc(area)) |> 
  unnest_wider(col = c(c1, c2), names_sep = "_") -> part2
# part2 has the areas of every possible rectangle

# make the rectangle simple feature from coordinates
makeRect <- function(i) {
  #i <- 1
  matrect <- tibble(x = c(part2$c1_1[i], part2$c2_1[i],
                          part2$c1_1[i], part2$c2_1[i]),
                    y = c(part2$c1_2[i], part2$c2_2[i],
                          part2$c2_2[i], part2$c1_2[i]))[c(1,3,2,4),] |>
    as.matrix()
  sf_rect <- st_as_sf(SpatialPolygons(list(Polygons(list(Polygon(matrect)), ID = i))))
  return(sf_rect)
}

tic()
# from largest, look for first valid rectangle
for( i in seq_len(nrow(part2))) {
  # create the sf rectangle
  rect_sp <- makeRect(i)
  
  # see if it's fully covered
  covres <- st_covers(green_area,rect_sp)[[1]]
  
  # some progress visualization
  if (i == 1) {
    plot(green_area, col="green4")
  }
  if (i %% 1000 == 0) {
    plot(rect_sp, border="red4", add=TRUE)
    message(paste(round(i/nrow(part2) * 100, 3), "% of rectangles evaluated so far"))
  }
  
  # if it's valid break, we're done
  if (length(covres) == 1 && covres == 1) {
    break
  }
}
toc()

# show results
largest_valid_area <- max(part2[i,"area"])
print(paste("Maximum area is:", largest_valid_area))

plot(green_area, col="green4")
plot(rect_sp, add=TRUE, col="red4")
