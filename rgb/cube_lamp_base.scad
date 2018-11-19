edge = 80;
edge_base = 83;
height_base = 18;
indent = 10;

difference(){
    linear_extrude(height = height_base + indent)
        square([edge_base, edge_base], center=true);
    union(){
        translate([0, 0, height_base])
            linear_extrude(height = height_base)
                square([edge, edge], , center=true);
        translate([0, 0, 5])
            linear_extrude(height = height_base)
                square([edge-5, edge-5], , center=true);
        translate([0, 7.5, 1])
            linear_extrude(height = height_base)
                square([40, 2], , center=true);
        translate([0, -7.5, 1])
            linear_extrude(height = height_base)
                square([40, 2], , center=true);
        translate([edge_base / 2, 0, 7])
            linear_extrude(height = 7)
                square([10, 4], , center=true);
    }
}