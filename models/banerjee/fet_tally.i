[Problem]
  [Tallies]
    [fet_mesh_tally]
      type = FETMeshTally
      order = 2
      score = 'flux kappa_fission'
      name = 'fet_flux fet_kappa_fission'
      normalize_by_global_tally = false
      check_tally_sum = false
      family = L2_LAGRANGE
      nodal_variable_order = FIRST
    []
   []
[]
