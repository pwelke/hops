graph [
  name "/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/PATTERNS/PATTERNS_IMDB/initial_3/imdbpattern_bca9ab8901e745b280f22b44a90e04ad/imdbpattern_bca9ab8901e745b280f22b44a90e04ad.gml"
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
    label "gender = Female"
    predicate "gender"
    target 0
    valueinpattern 1
    type "None"
    value "Female"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 2
    target 3
  ]
]
