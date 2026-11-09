
[Problem]
    [Tallies]
        [mesh_tally]
          type = MeshTally
          score = 'flux kappa_fission'
          name = 'flux kappa_fission'
          normalize_by_global_tally = false
          check_tally_sum = false
           output  = 'unrelaxed_tally_std_dev unrelaxed_tally_rel_error'
        []
    []
[]

[VectorPostprocessors]
  [tally_value]
    type = LineValueSampler
    variable = "flux flux_rel_error"
    sort_by = 'x'
    start_point = '0.00001 0 0'
    end_point = '14 0 0'
    num_points = 1000
  []

[]
