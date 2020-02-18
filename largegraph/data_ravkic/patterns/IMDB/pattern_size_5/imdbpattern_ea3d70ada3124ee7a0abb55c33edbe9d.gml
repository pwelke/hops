graph [
  name "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_4/batch3/imdbpattern_eb2d1d49cfb6421ea1457b4c464bdbef/imdbpattern_eb2d1d49cfb6421ea1457b4c464bdbef.parent"
  node [
    id 0
    label "genre"
    predicate "genre"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "movie"
    predicate "movie"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "director"
    predicate "director"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "actor"
    predicate "actor"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "gender = Male"
    predicate "gender"
    target 0
    valueinpattern 1
    type "None"
    value "Male"
  ]
  edge [
    source 0
    target 2
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 1
    target 3
  ]
  edge [
    source 3
    target 4
  ]
]
