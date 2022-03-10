# Pattern for Simple Sweater for Rhein Knit
# November 2021, akj
# First iteration

import gauges
import math
import sizes

# Medium weight yarn (combinations): 14-20sts.
# should accomodate all (or the most frequent sts/row combinations)

# Cast on x stitches
# Knit n height rib, then m height stockinette
# Decrease for armpit, y sts over k rows (leave 1 km on either side)
# Knit p height for chest
# BO center stitches for neck
# Dec against neck (all completed at w cm to go for full height)

# BO l shoulder stitches over w cm
# Sew the shoulder seam together with madras sting
# PU a stitches along the armhole edge (x sts/rows for n cm)
# Knit p cm while decreasing 2 sts on each z row. 
# Change to smaller needles and knit 1*1 ribbing for n cm.
# Bind off loosely and sew together the armpit and all loose ends.
# Enjoy.


class SimpleSweater:

	def __init__(self, gauge, size):

		self.size = size
		self.gauge_sts = gauge["sts"]
		self.gauge_rows = gauge["rows"]

		# Assertions
		assert(self.size["height"]["total_length"] == self.size["height"]["body_to_underarm"] + self.size["height"]["armhole"] + self.size["height"]["shoulder"])
		assert(self.size["width"]["hip"] == self.size["width"]["neck"] + (self.size["width"]["shoulder"]+self.size["width"]["armpit"]) * 2)
		
		# CO and Body
		cast_on_sts = self.ensure_div4((self.size["width"]["hip"]*2)*self.gauge_sts)

		self.body = f'Cast on {cast_on_sts} stitches on smaller needles and knit {round(self.size["height"]["rib_at_body"])} cm 1*1 ribbing (1 knit, 1 purl). '
		self.body += f'Change to larger needles. On the next row, place stitch marker at the beginning of round, knit {round(cast_on_sts/2)} sts, place stitch marker, knit {round(cast_on_sts/2)}. These stitch markers mark the sides of your garment. '
		self.body += f'Continue knitting stockinette in the round until your garment measures {round(self.size["height"]["body_to_underarm"])}cm from the cast on edge. ' 
		self.body += f'We will now BO for the armpits and seperate the garment in a front piece and a back piece. '
		
		# Armpits
		armpit_sts = self.ensure_even(self.size["width"]["armpit"] * self.gauge_sts)
		armpit_rows = self.ensure_even(self.size["height"]["armpit"] * self.gauge_rows)
		armpit_bo = self._angled_armhole_bindoffs(armpit_rows, armpit_sts)
		initial_armpit_bo = str(armpit_bo[0])
		
		self.front =  f'On the next row, BO {initial_armpit_bo} sts and knit to the marker. The stitches you have just worked form your front piece. Place the next {round(cast_on_sts/2)} sts on a stitch holder or scrap yarn. These stitches form your back piece and will be left to rest for now. '
		self.front += f'Next row (wrong side), BO {initial_armpit_bo} sts and purl to the end. '
		self.front += f'BO ({", ".join(str(x) for x in armpit_bo[1:])}) on the next {len(armpit_bo)-1} rows from either side. '
		self.front += f'Continue knitting {self.size["height"]["armhole"]-self.size["height"]["neck_front"]}cm back and forth in stockinette until your front piece measures {self.size["height"]["total_length"]-self.size["height"]["neck_front"]} cm. '
		
		self.back =  f'Pick up the {round(cast_on_sts/2)} back piece sts. '
		self.back += f'Starting with a right side row, BO {initial_armpit_bo} sts and knit to the end. Next row (wrong side), BO {initial_armpit_bo} sts and purl to the end. '
		self.back += f'Continue binding off as you did on the front:  ({", ".join(str(x) for x in armpit_bo[1:])}) on the next {len(armpit_bo)-1} rows from either side. ' 
		self.back += f'Continue knitting {self.size["height"]["armhole"]-self.size["height"]["neck_back"]}cm back and forth in stockinette until your back piece measures {self.size["height"]["total_length"]-self.size["height"]["neck_back"]} cm. End with a wrong side row. '
		
		# Neck
		neck_sts = self.ensure_even(self.size["width"]["neck"] * self.gauge_sts)

		# decreases should be completed at 50% of the height of the neck to ensure the dec are not spread out to much 
		# and that the shoulders are created seperately.
		# Also decreases only occur on every other row.
		neck_dec_rows_front = round(((self.size["height"]["neck_front"] / 2)/ 2 ) * self.gauge_rows)
		neck_dec_rows_back = round(((self.size["height"]["neck_back"] / 2)/ 2) * self.gauge_rows)

		# Shoulder sts are calculated based on cast on sts and armpit BOs, not directly from the size["width"]["shoulder"]
		shoulder_sts = ((cast_on_sts/2)-(2*sum(armpit_bo))-neck_sts) / 2
		shoulder_dec_rows = round((self.size["height"]["shoulder"] / 2) * self.gauge_rows)

		front_bos = self._crew_neck_front(neck_sts, neck_dec_rows_front)
		
		self.front += f'On the next row, knit {round(shoulder_sts+sum(front_bos[1:]))} sts, BO center {front_bos[0]} sts, and knit to the end. '
		self.front += f'Continue knitting back and forth over these stithes for the right front shoulder. BO {front_bos[1:]} sts at the begining of the next {len(front_bos[1:])} right side rows. '
		self.front += f'You now have {int(shoulder_sts)} sts left on your needles for right front shoulder. Knit {neck_dec_rows_front}cm straight up, ending with a right side row. '

		back_bos = self._crew_neck_back(neck_sts, neck_dec_rows_back)
		self.back += f'On the next row, knit {round(shoulder_sts+sum(back_bos[1:]))} sts, BO center {back_bos[1]} sts, and knit to the end. '
		self.back += f'Continue knitting back and forth over these stithes for the left back shoulder. BO {back_bos[1:]} sts at the begining of the next {len(back_bos[1:])} right side rows. '
		self.back += f'You now have {int(shoulder_sts)} sts left on your needles for left back shoulder. Knit {neck_dec_rows_back}cm straight up, ending with a right side row. '
		
		self.shoulder_bo = self._shoulder_shaping(shoulder_sts, shoulder_dec_rows)
		self.front += f'On the next (wrong side) row, BO {self.shoulder_bo[0]} sts, purl to the end. Knit the next row. Continue in this way, binding off {self.shoulder_bo[1:]} on the next {len(self.shoulder_bo)-1} row(s) and knitting the right side rows. '
		self.front += f'Complete the left front neck and shoulder in the same manner. NB: since the left front is mirrored, you will BO for the neck on the wrong sides, and BO for the shoulders on the right sides. '
		self.back +=  f'On the next (wrong side) row, BO {self.shoulder_bo[0]} sts. Knit the next row. Continue in this way, binding off {self.shoulder_bo[1:]} on the next {len(self.shoulder_bo)-1} row(s) and knitting the right side rows. '
		self.back +=  f'\nComplete the right back neck and shoulder in the same manner. NB: since the right back is mirrored, you will BO for the neck on the wrong sides, and BO for the shoulders on the right sides. '
		
		self.sleeves = ''
		# KANTMASKER
		print("BODY\n", self.body)
		print("FRONT\n", self.front)
		print("BACK\n",self.back)

	def _crew_neck_front(self, neck_sts, neck_front_rows):
		# The stitches to decrease must be an even number and will be split over the two sides of the neck shaping, i.e. half of the stitches will be decreased on each side of the initial bindoff.
		# First, bind off 30% of stitches_to_decrease, then another third of what is over and then singles.
		
		# Bind off 1/3 of the neck stitches.
		initial_bo = self.ensure_even(neck_sts/3)
		dec_sts_per_side = round((neck_sts - initial_bo)/2)
		neck_front_rows -= 1
		mod = dec_sts_per_side % neck_front_rows
		if mod == 0:
			bos = [int(dec_sts_per_side/neck_front_rows)] * neck_front_rows
		else: 
			print(dec_sts_per_side, neck_front_rows)
			if (dec_sts_per_side-mod) % neck_front_rows == 0:
				bos = [int((dec_sts_per_side-mod)/neck_front_rows)] * neck_front_rows
				bos[0] += int(mod)
		front_bos = [initial_bo] + bos
		return front_bos
	
	def _crew_neck_back(self, neck_sts, neck_back_rows):
		# The stitches to decrease must be an even number and will be split over the two sides of the neck shaping, i.e. half of the stitches will be decreased on each side of the initial bindoff.
		# First, bind off 30% of stitches_to_decrease, then another third of what is over and then singles.
		
		# Bind off 1/3 of the neck stitches.
		initial_bo = self.ensure_even(neck_sts/3)
		dec_sts_per_side = round((neck_sts - initial_bo)/2)
		
		# Remaining bind offs:
		mod = dec_sts_per_side % neck_back_rows
		if mod == 0:
			bos = [int(dec_sts_per_side/neck_back_rows)] * neck_back_rows
		else: 
			if (dec_sts_per_side-mod) % neck_back_rows == 0:
				bos = [int((dec_sts_per_side-mod)/neck_back_rows)] * neck_back_rows
				bos[0] += int(mod)
		back_bos = [initial_bo] + bos
		return back_bos
		
	def _shoulder_shaping(self, shoulder_sts, shoulder_rows):
		# sunken shoulders

		mod = shoulder_sts % shoulder_rows
		if mod == 0:
			bos = [int(shoulder_sts/shoulder_rows)] * shoulder_rows
		else: 
			if (shoulder_sts-mod) % shoulder_rows == 0:
				bos = [int((shoulder_sts-mod)/shoulder_rows)] * shoulder_rows
				bos[0] += int(mod)
		return bos

	def _angled_armhole_bindoffs(self, armpit_rows, armpit_sts):
		# Get the bind offs for angled bind off.
		bindoffs = [0] * armpit_rows
		for n in range(len(bindoffs)):
			if n == 0:
				bindoffs[n] = math.ceil(armpit_sts/2)
				armpit_sts - bindoffs[n]
			else:
				bindoffs[n] = math.ceil((armpit_sts-sum(bindoffs))/2)
				armpit_sts - bindoffs[n]
		bindoffs = [x for x in bindoffs if x != 0]
		return bindoffs

	def ensure_div4(self, num):
		num = math.floor(num)
		div4 = num % 4
		if div4 == 0:
			return num
		elif (num+div4) % 4 == 0 and (num+div4) % 2 == 0: 
			return (num+div4)
		elif (num+1) % 4 == 0:
			return num+1
		else:
			print('Cast on error, not dividable by 4')
			return 0

	def ensure_even(self, num):
		num = math.floor(num)
		return num+(num % 2)
# Test examples
size = sizes.medium_man
gauge = gauges.double_spindrift
pattern = SimpleSweater(gauge, size)

# size = sizes.medium_man
# gauge = gauges.kos
# pattern = SimpleSweater(gauge, size)

