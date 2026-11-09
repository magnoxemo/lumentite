!include fet_tally.i

[Mesh]
  [fmg]
    type = FileMeshGenerator
    file = 'mesh_in.e'
  []
[]



[Problem]
  type = OpenMCCellAverageProblem
  initial_properties = xml
  power = 10000
  source_rate_normalization = kappa_fission
  particles=40000
[]

[Executioner]
  type = Transient
  num_steps = 1
[]

[Outputs]
  exodus = true
  csv=true
[]
