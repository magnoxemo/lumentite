[Mesh]
  final_generator = center
  [slab_stack]
    type = CartesianMeshGenerator
    dim = 3
    dx = '0.5 1 1 1 1 1 1 1 1 1 1 1 1 1 0.5'
    ix = '2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 '
    dy = 1
    iy = 1
    dz = 1
    iz = 1
    subdomain_id = '1 2 1 2 1 2 1 3 1 2 1 2 1 2 1'
  []
  [rename_blocks]
    type = RenameBlockGenerator
    input = slab_stack
    old_block = '1 2 3'
    new_block = 'moderator fuel absorber'
  []
  [convert]
    type = ElementsToTetrahedronsConverter
    input = rename_blocks
  []
  [center]
    type = TransformGenerator
    input = convert
    transform = TRANSLATE
    vector_value = '0 -0.5 -0.5'
  []
   [refine_mesh]
       type=RefineBlockGenerator
       input=center
       block="moderator fuel absorber"
       refinement=0
  []
[]
