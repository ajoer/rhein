# Measurements here are garment measurements, not body measurements

medium_man = { # total_length = body_to_underarm + armhole + shoulder (this is highest point, at neck opening.)
	"height" : { # * ROWS 
		"total_length": 65, # from cast on to shoulder. Full length of garment (including ribbing)
		"body_to_underarm": 41.5, # from cast on edge to underarm
		"body_to_waist": 21, # from cast on to waist
		"waist_to_underarm": 20.5, # from waist to underarm
		"neck_front" : 7,
		"neck_back": 3,
		"armpit": 6,
		"armhole" : 22, # from underarm to top of shoulder
		"shoulder" : 1.5, # height of shaping shoulder 
		"sleeve": 40, # sleeve length without rib
		"rib_at_body": 6, # ribbing at hip
		"rib_at_wrist": 6, # ribbing at wrist
		"rib_at_neck": 2.5, # ribbing at wrist
		
	},
	"width" : { # * STITCHES # hip == neck_front + (shoulder+armpit) * 2
		"hip" : 52, # half torso measured at bottom of garment (above rib)
		"waist": 52, # half torso measured at waist
		"bust": 52, # half torso measured at bust
		"neck": 20, # neck opening at top = 45% of cross back width
		"shoulder": 12, # shoulder width at top
		"armpit": 4,
		"upperarm": 44, # sleeve width at top --- must be same as armhole height * 2
		"sleeve_at_wrist": 26, # sleeve at wrist, above ribbing
	}
}