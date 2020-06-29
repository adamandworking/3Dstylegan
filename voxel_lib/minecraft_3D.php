<?php
include_once realpath(dirname(__FILE__) . '/3d.php');
	
$player = new render3DPlayer('', '-25', '25', '10', '10', '-10', '20', '5', 'true', 'false', 'png', '12', 'true', 'true');
//render3DPlayer(user, vr, hr, hrh, vrll, vrrl, vrla, vrra, displayHair, headOnly, format, ratio, aa, layers)
$png = $player->fallback_img = 'voxel_lib/cache/tmp.png';
$png = $player->get3DRender();
imagepng($png, 'voxel_lib/cache/tmp_gen.png');
