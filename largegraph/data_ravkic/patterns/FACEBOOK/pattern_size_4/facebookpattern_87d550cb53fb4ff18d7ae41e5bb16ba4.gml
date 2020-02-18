graph [
  name "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_FACEBOOK//patterns_size_3/batch1/facebookpattern_a4c1853a6391445cbfebb3f50c8eb548/facebookpattern_a4c1853a6391445cbfebb3f50c8eb548.parent"
  node [
    id 0
    label "education_degree"
    predicate "education_degree"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "user"
    predicate "user"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "birthday"
    predicate "birthday"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "education_type = value_unknown"
    predicate "education_type"
    target 0
    valueinpattern 1
    type "None"
    value "value_unknown"
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
    source 1
    target 3
  ]
]
