graph [
  name "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_4/batch5/imdbpattern_bba7081293414103b0702341bd2fa8aa/imdbpattern_bba7081293414103b0702341bd2fa8aa.parent"
  node [
    id 0
    label "gender"
    predicate "gender"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "director"
    predicate "director"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "actor"
    predicate "actor"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "movie"
    predicate "movie"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "genre = Acrime"
    predicate "genre"
    target 0
    valueinpattern 1
    type "None"
    value "Acrime"
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
    target 4
  ]
  edge [
    source 2
    target 3
  ]
]
