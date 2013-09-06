#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import tornado.ioloop
import tornado.web
import tornado.auth
from tornado.escape import json_encode, json_decode
from tornado.options import define, options

define('on_port', default=8000, help="Run on port")

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		user = self.get_secure_cookie('user_id')
		if user:
			return json_decode(user)
		else:
			return None

class MainHandler(BaseHandler):
    def get(self):
    	user = self.get_current_user()
    	if user:
    		self.write("<a href=\"/bye-bye\">disable retweets for everyone</a>")
        else:
            self.write("<a href=\"/sign-in\">sign in</a>")


class SignInHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie('user_id', json_encode(user))
            self.redirect("/")
        else:
            yield self.authorize_redirect()

class SignOutHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_secure_cookie('user_id', None)
        return self.redirect("/")

class ByeByeHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #get everyone i follow
        friend_ids = yield self.twitter_request(
            "/friends/ids",
            count=5000,
            access_token=self.current_user["access_token"])
        #friend_ids = {u'previous_cursor': 0, u'previous_cursor_str': u'0', u'next_cursor': 0, u'ids': [14501411, 5622, 2022521, 1599732272, 327775450, 444645230, 12971042, 68127718, 3162831, 35855886, 880022736, 23275810, 26928431, 18699939, 383751455, 248885215, 1028148042, 26836282, 865926859, 1037622697, 1036041637, 1041217896, 1028315532, 36973752, 820403708, 14127833, 247117592, 2569691, 44809334, 91388995, 110453381, 305334797, 294331193, 1054209054, 1086367316, 65683, 41403898, 486343196, 332313339, 234263070, 1046758885, 975467275, 247652231, 1126058154, 87793812, 93472467, 112631010, 1688741, 43268012, 13303832, 390351418, 32872603, 281284002, 31491438, 92659714, 328948735, 34415851, 739367892, 352775461, 186689040, 791865272, 1058831395, 84016634, 31494769, 784975052, 155137048, 99382324, 102272719, 1172862558, 15657025, 191297606, 52590907, 9973242, 21100195, 32238892, 114954667, 10106042, 14636627, 68103775, 2214291, 16389719, 18060279, 282827622, 25220410, 200196715, 902813664, 748268642, 938657858, 799292, 590450944, 18040878, 68559415, 176084642, 6649362, 14687572, 17330584, 813333008, 121989300, 18852596, 538883407, 70168483, 1215207853, 560319296, 6832532, 1500041, 519793477, 156020838, 737559986, 111636511, 145010371, 14417215, 343949881, 9254512, 90981935, 789090414, 299789736, 14231566, 454434921, 66122442, 390970453, 415764213, 393193208, 20900044, 20387097, 226351221, 51670810, 76640116, 47470976, 14907376, 259814081, 38692059, 11678, 393508037, 399396402, 399520021, 258069484, 14569192, 384792461, 388483845, 5676212, 345891234, 46713, 346579898, 401167021, 384791343, 401885576, 376356097, 16646727, 327747046, 402720077, 393711196, 18893, 177242396, 24583, 29598598, 15950645, 256766293, 169976767, 405779988, 86258170, 406849512, 755385, 289859263, 94949184, 135000502, 410735919, 263751035, 365172979, 17488114, 403688301, 46718643, 294573197, 150, 37047050, 285354758, 372653139, 397556058, 230290968, 96275016, 415542228, 623213, 415087416, 416333186, 17920946, 17295035, 417770391, 418713113, 2427711, 17533464, 422807453, 14454667, 24553114, 377490410, 289571349, 1155401, 1594021, 400490987, 324846701, 1570611, 428483494, 3574921, 29005390, 15467416, 15970085, 24622810, 13132602, 129586119, 789866, 420128977, 14902356, 3438881, 292593848, 274615957, 661863, 22425392, 153277475, 430292386, 17823816, 221519276, 45849351, 19455351, 404196923, 93112774, 378091704, 148846434, 214527138, 130607305, 15204677, 3250841, 21049643, 20175080, 16788990, 25888758, 16138920, 435133920, 17796231, 433106378, 7324992, 324447873, 335966904, 14299324, 15309940, 32650523, 327985466, 16329747, 22616406, 14189573, 20854859, 19366041, 126243784, 14090660, 105206835, 61258626, 330080317, 112666986, 17194589, 347429487, 112552110, 31087189, 395905523, 18713102, 78027337, 11317672, 26458720, 18455818, 41464966, 440654710, 3404, 333025694, 28652943, 44802012, 18336444, 14722254, 315877586, 15586035, 64680531, 18232376, 19930926, 45068191, 104713368, 11427402, 20767736, 175346837, 450691429, 15079373, 16179850, 360107408, 93909252, 27324361, 5823382, 6853512, 456238604, 14808481, 445953699, 161723960, 378581677, 457447713, 158449764, 87871580, 14508998, 459826258, 11279812, 460361987, 460479783, 460774147, 11964, 461268560, 6532, 41098791, 152418335, 221131215, 17311542, 462551270, 462657741, 462659148, 462699019, 462783229, 288206798, 462866472, 302235157, 463224196, 463239377, 463475003, 412610656, 19455010, 458537931, 135702780, 799430, 139846098, 9973572, 195998517, 8874252, 3330, 14209369, 15576134, 10102222, 96514540, 463598092, 11084522, 470667272, 160063119, 14120760, 157494698, 14548212, 61549545, 114873142, 449520288, 7442732, 14134365, 20607502, 473290848, 149865112, 358700898, 1960791, 404278100, 293116919, 454607410, 208060004, 154108110, 1154511, 19002462, 15872144, 365269757, 14258985, 404065065, 14241401, 203041211, 483524924, 14135108, 75744308, 17887099, 23139790, 41837082, 99202474, 485835142, 301509948, 476641949, 341815784, 82705484, 5790592, 24288307, 19563939, 410648827, 49538645, 35173092, 196179103, 138609362, 160467872, 67807135, 493738592, 5029521, 55525953, 10806002, 11407702, 12534, 14365077, 20830775, 385192192, 31910949, 24744709, 850, 6129732, 384800359, 878471, 375875804, 211935905, 170677676, 28815085, 14293709, 174018997, 15120464, 125512980, 17534056, 81560164, 289723545, 18953693, 388168954, 226238536, 173437953, 357962418, 16625092, 15384619, 67481433, 221663371, 90121914, 15878314, 767637, 13524672, 122190528, 353123498, 10631912, 32404803, 135259297, 15080807, 384703382, 21969268, 385197739, 313960718, 196847956, 14772863, 15866967, 12633942, 17076243, 14282140, 145354533, 314713859, 15584619, 21649731, 15003, 30863, 197278508, 300564408, 11387592, 1544881, 22890557, 469073, 710133, 394740921, 230374525, 230121102, 6484462, 260317645, 14498997, 47140912, 378143228, 18687829, 14827507, 14685595, 95563, 75086697, 302239582, 397893584, 393087133, 1172651, 9252932, 88199448, 398415923, 46121701, 398602207, 11388382, 103943240, 14403212, 44297590, 15103795, 20047494, 159422449, 93135816, 40315411, 16422162, 32463152, 9404392, 44128472, 273842092, 24292393, 264516214, 25808530, 18999001, 14276320, 334471893, 19999563, 355128353, 29611346, 8146392, 14184631, 15531113, 83742576, 356517445, 340798984, 184189095, 641073, 29638408, 116308926, 38623, 345983482, 155520050, 184000792, 20224827, 293024264, 8008452, 190860973, 18342316, 14840267, 26464972, 37834616, 15516456, 266944905, 18698672, 28688030, 344982427, 321510330, 86387453, 20576130, 23019386, 22693434, 14562031, 32174199, 26357567, 39736888, 17410733, 24658124, 21295480, 17260321, 163370236, 325187191, 10621922, 301619365, 79966746, 90944799, 82551195, 344647472, 1778601, 18348947, 15271526, 7665512, 19715087, 15032983, 102787175, 360486517, 14666247, 237256592, 7569872, 1122911, 75086322, 16637215, 17295625, 14185781, 23162900, 18744400, 5107, 128137476, 211307909, 228211279, 237776611, 17286492, 274945615, 14398606, 297481735, 16405408, 189282302, 88680453, 173429362, 17971297, 260971417, 11136252, 14377062, 73664572, 157984269, 14101542, 15958353, 209447304, 86788422, 325929308, 206152778, 22097987, 70318789, 14487298, 224740109, 351972051, 166324647, 268439041, 28750955, 6655452, 371654630, 23998385, 59606023, 78469615, 19076143, 82661220, 10651312, 377332823, 194722345, 39572272, 17838681, 85919546, 377172254, 26024221, 376824630, 1738031, 120005054, 279362623, 330757281, 14084390, 14776405, 278800364, 109461052, 420493, 32185320, 5570262, 16411813, 666713, 256443696, 34603, 193317756, 381239593, 35233, 49675112, 357266509, 26172254, 4071601, 54537977, 359744753, 371934721, 371988336, 281497643, 80464499, 303810268, 373429151, 14447884, 14965418, 3300, 345446064, 348409952, 28159507, 323975726, 23793342, 1592491, 365738401, 225592963, 367309731, 7547012, 99905635, 15264854, 329556701, 329526432, 329552482, 329546885, 789659, 2230561, 212324810, 104623, 8162752, 55904488, 6714782, 16275037, 20982426, 93719528, 42954055, 15447585, 273808390, 14301605, 129073124, 333752114, 51863141, 14513945, 184178386, 755984, 14697227, 299837277, 3662291, 335412166, 21473622, 95453826, 17753016, 207818951, 19714153, 769920, 337210779, 219907434, 23278879, 20459650, 329388327, 329492528, 15617393, 21856443, 94579246, 340348906, 14836174, 18151322, 34949045, 10967, 159184107, 340770076, 213785407, 81683878, 19870960, 21764378, 24163453, 12442362, 14162146, 167871088, 47285170, 15937978, 46616976, 202288409, 18756509, 19012787, 276189775, 15428857, 272172139, 16149868, 15862493, 77832365, 14522529, 27140182, 14430993, 102094177, 83094570, 347299259, 293436088, 347813865, 23180603, 8216772, 7372902, 7160892, 206055381, 10338902, 7114842, 59702505, 279161279, 345737342, 246878512, 96871242, 351196224, 340291126, 126340746, 208101288, 49496222, 146205445, 9125482, 333265815, 256435658, 10157802, 8546472, 132653965, 352800736, 19476518, 16165721, 19087496, 19687696, 307728990, 16007158, 48281562, 39546755, 14989648, 106957422, 247980523, 291363, 7311762, 37926806, 797546, 12284, 469163, 2030231, 19131896, 104613815, 17896640, 39192805, 14053254, 179853237, 6609452, 271131911, 32174717, 14331292, 16285622, 64099075, 17163460, 9497862, 1516381, 154493778, 274957941, 17112954, 5683402, 4534071, 22406671, 7235512, 325182030, 184533645, 656233, 6576662, 16620786, 12997772, 16742858, 5414172, 17473931, 15235774, 1659201, 55343615, 243131890, 12057012, 24063, 1199121, 15419004, 14639162, 12204772, 5118401, 14117595, 16798339, 12919902, 22255339, 1872611, 319266757, 37631449, 1741681, 18663556, 14058346, 748163, 14577178, 318769986, 14327598, 3096591, 20914879, 9765902, 18621891, 304224500, 17431441, 15403952, 39899124, 52296298, 330062991, 40771479, 329380326, 448, 231018076, 1338321, 248200454, 136605760, 34713, 1518031, 12803032, 47333409, 54535167, 5644842, 25569158, 323124534, 5034, 306569242, 59837317, 49586293, 15751803, 23204337, 333262775, 146264889, 255458198, 307648564, 41931019, 20680765, 51631511, 6119752, 37992360, 10115802, 14913849, 7841702, 140891152, 29283, 312613342, 136343077, 9027, 11069002, 7738782, 14147202, 14339186, 14578867, 261529424, 16555679, 755768, 32055904, 35253, 17058682, 341, 245379961, 35521202, 4711, 244372151, 75785885, 5443752, 21740509, 25864057, 27307180, 315755621, 105787191, 14140044, 169600168, 212327199, 37287365, 139538040, 319792114, 13243822, 1307381, 58323, 320846226, 14799178, 85710782, 10282782, 247409525, 14279363, 60641365, 619843, 18216157, 12733192, 15395001, 110775132, 16578992, 14461207, 16530945, 144112977, 24486084, 113401802, 21658268, 21385609, 14007992, 15639933, 833981, 9078992, 35519997, 5865212, 98702688, 3913081, 4335271, 26776079, 15456437, 7111002, 2691, 15589459, 78370614, 278371635, 10326732, 11262, 14442079, 16115216, 28905307, 312474728, 699443, 22330951, 163439723, 11753, 246352275, 7035712, 15683885, 816640, 15057438, 14239791, 66227095, 15231426, 300596619, 14600546, 10847772, 38220899, 265002075, 1596141, 188984879, 14119103, 984931, 21791847, 14682618, 19806605, 14578014, 223991592, 19122310, 23619273, 20263, 25321582, 52503670, 14473069, 14301764, 16851665, 14757313, 309369028, 636743, 7552662, 768238, 787081, 11264602, 781386, 1761301, 62105112, 14919491, 14830887, 964111, 3969131, 12921162, 18357906, 1798581, 14537680, 15587262, 81890111, 10647162, 74737515, 52773, 113432154, 34943, 51373, 12797, 4222161, 57122080, 211275718, 33535416, 9396402, 176316063, 14930058, 6772522, 12662152, 655893, 240707175, 7258112, 55275099, 7433022, 20968053, 73681907, 306393323, 247027846, 802568, 122151994, 15496615, 14835480, 287182640, 15229273, 16069103, 213664267, 7492672, 108245197, 23748717, 135766019, 162401830, 20105081, 17525942, 230009024, 15719107, 15037090, 974121, 297246888, 216203560, 15015733, 1330271, 253036721, 1535441, 9285962, 15992368, 89388888, 290604295, 7836, 8699982, 31215241, 36043, 8123792, 15412788, 21277315, 4114251, 27143441, 26886969, 313280052, 195432548, 6505442, 5815592, 15218891, 17203940, 132685619, 314493173, 228287992, 68799566, 314693534, 34254982, 14157059, 88525515, 37594784, 6187652, 16853, 46090477, 287069836, 180342373, 305183556, 15214243, 14742479, 316198003, 255353858, 641673, 190315863, 25038598, 284759293, 14968097, 37474126, 54081321, 7601962, 112563221, 26167276, 18593513, 14074757, 14445272, 219470050, 673093, 220343922, 287187967, 14155960, 182584657, 17499350, 930061, 740763, 15789421, 310136335, 307319494, 217495853, 11203612, 201000644, 19963247, 84459540, 809399, 13697, 14290652, 15004131, 96582608, 16861749, 27790437, 175372721, 205450379, 420193, 35303670, 57708899, 256293846, 643613, 16631482, 8168122, 243774916, 24700489, 35623579, 16372389, 234254972, 1481631, 9619972, 138821636, 25663, 16102748, 74253, 281609027, 5674602, 3087901, 2616111, 15596499, 19451277, 298960178, 1887491, 118800349, 208171489, 24407198, 34041549, 740683, 292401329, 111628416, 38711108, 16150053, 5937722, 143569237, 6787612, 6790312, 14445819, 183813, 231458313, 142465240, 699183, 16856958, 114146208, 30348363, 16739915, 217175560, 66218811, 16810307, 14475802, 23823589, 683033, 130418225, 8037402, 18209839, 114425208, 304982760, 27281198, 17976723, 170625929, 45604122, 6257562, 5861982, 19463460, 11101232, 293840943, 16492516, 97809456, 7698162, 154378419, 17959369, 14407694, 6140982, 222601296, 14033052, 14907456, 85090229, 49092609, 38143, 14422457, 21270495, 54594000, 34863, 16140843, 2267431, 24322876, 14624900, 37873, 18492424, 7490602, 18901818, 23900208, 18959173, 7678702, 19706643, 19387902, 2374211, 94496379, 18940889, 15158420, 685063, 5101261, 14233693, 44941718, 18799688, 19577620, 246239102, 235209268, 16044876, 105608388, 9516092, 247982441, 37306920, 6653172, 14532029, 298101500, 15838862, 236923679, 18350445, 271121007, 158250423, 649633, 6436, 28452302, 12188, 8648882, 15593231, 2125931, 4897, 14604055, 8010542, 820569, 9109122, 18524949, 7083152, 21430653, 5794742, 1260091, 6774052, 15787206, 25436481, 15379880, 15652414, 14195773, 5702262, 8936032, 14259188, 108181757, 950551, 13171312, 20278453, 17670603, 14254028, 16729566, 16280791, 286331003, 10839172, 641233, 8689872, 9869382, 5692142, 2359731, 16729673, 277210572, 19126362, 234127602, 49710326, 289207597, 255350633, 716863, 7193752, 35546258, 24054339, 14185745, 232002424, 15795938, 279945159, 21250871, 20959538, 123551728, 2569881, 158425943, 25828723, 3549571, 50268764, 151813107, 774438, 5602282, 89309285, 14334580, 48903480, 217693353, 122970860, 25544623, 19874197, 19488810, 2765491, 75473841, 8892, 14898776, 31235568, 221519764, 298635388, 280769362, 14590690, 129562249, 233464344, 37454491, 19486897, 14125107, 13472402, 16588258, 13278842, 14726716, 19168111, 48901814, 21734901, 10108162, 2038451, 11682952, 9896672, 6756352, 14957429, 118963, 22196723, 14823283, 14086661, 1461211, 58569600, 15593522, 173613245, 14337777, 101614929, 19563837, 60136288, 141381979, 65362661, 14725156, 618233, 27253037, 13261402, 198197979, 86864976, 113181578, 109000872, 809610, 83568175, 20809194, 15108094, 184554581, 46009102, 167168744, 9127902, 14975979, 84136842, 92015003, 15844722, 46082263, 29831897, 14095302, 18297449, 817224, 14412361, 14579124, 21674530, 14679398, 30507583, 134945001, 42478061, 51647515, 110127142, 4530881, 150225676, 237795114, 66951315, 14314775, 15885345, 154144410, 13267712, 1222751, 22453, 18647785, 9063542, 19564044, 46615059, 17377337, 69818163, 240395670, 13210402, 25268969, 13439, 785138, 24342828, 14789498, 9043992, 49190773, 6688272, 10187132, 12044902, 16204643, 16337631, 15421449, 28221603, 9624942, 297158655, 35311053, 8038612, 15105114, 16653306, 15350091, 22873770, 24851115, 102119907, 640393, 67024657, 164532432, 4214321, 56798857, 5812852, 816810, 40277243, 22112285, 78623673, 14997986, 17924036, 271839920, 6883662, 23074474, 680433, 14216805, 14588838, 21478323, 44217930, 3927591, 18078513, 15519691, 116944326, 8083772, 65943868, 1266241, 1481091, 100321244, 720533, 172283494, 120605562, 17781599, 643143, 33258259, 817452, 3821111, 15481845, 39653, 783935, 10748542, 20693, 19326481, 4872, 27215933, 47424461, 14455558, 251698386, 7854592, 63850630, 14438595, 17777757, 14533149, 17548111, 661243, 17011212, 28222025, 16062411, 146156967, 224382856, 42833, 30071662, 3623901, 277817713, 8017782, 14593841, 18519660, 6044592, 14221473, 16454182, 13548292, 241208763, 91038280, 714563, 3990481, 819797, 67042272, 14945780, 14291839, 8882, 12709182, 20462780, 2328421, 16068624, 14752818, 651963, 33909489, 16936110, 198267077, 18371906, 15655035, 130386571, 19159713, 33150690, 14413797, 25950160, 15651903, 9670142, 90731105, 5504052, 9128622, 15554673, 783909, 3583541, 4779551, 14301126, 9442562, 1912101, 13129062, 15695954, 139199207, 122052360, 2070321, 5929632, 14630373, 176057761, 36131760, 7832082, 289935842, 110600452, 6324042, 946521, 797078, 27139966, 10645092, 290181526, 5476632, 669883, 3312551, 30696075, 10044012, 78213, 6534262, 14667502, 14607811, 14305121, 246696204, 10919032, 6921022, 97049211, 16650306, 109160033, 7320232, 14812896, 4082611, 15081761, 89590749, 6417142, 198590804, 34015644, 749863, 77901235, 17628933, 18655890, 25814161, 4103881, 5439732, 80365335, 1941, 12924972, 731283, 21672658, 26758226, 2665, 1093901, 26571129, 3048, 20419027, 808264, 14590462, 15336076, 14247122, 32528963, 90738900, 67645636, 5348, 346, 60907976, 24072526, 1484411, 11219862, 5263, 18409628, 12155512, 36533, 677703, 5779102, 285986420, 19408269, 221977530, 18706471, 11947372, 14741894, 5631362, 12661, 2245401, 13482482, 8985752, 36211188, 15347746, 3640, 17004919, 14178698, 191334198, 15755614, 14826416, 15450708, 14159035, 777844, 2250271, 187354451, 965, 26941522, 14443071, 14147386, 282784033, 288619905, 1058051, 21364729, 972441, 18464631, 3106601, 205223548, 75979115, 263027757, 14782688, 58643168, 48891920, 89553140, 30799374, 14113799, 11405242, 280784346, 13472812, 7616432, 2549, 178548253, 656323, 61382550, 57474396, 119916149, 262064361, 277078875, 174798345, 83719783, 217083295, 25013674, 5630382, 861951, 5623222, 283780143, 196967497, 1385211, 19503926, 20552586, 12436, 15605892, 188891606, 22864506, 6709, 249506172, 1845731, 286082756, 235088575, 227155630, 109642332, 261091001, 44322721, 17934129, 8071902, 14861522, 84499588, 53097835, 16724894, 98499713, 1038, 136, 141536502, 15118998, 45141069, 36683236, 5999992, 135262466, 210216640, 5203191, 15233704, 26160420, 8752752, 21611935, 64993168, 816830, 15202126, 118793979, 22010644, 155279223, 16657879, 26906592, 270733980, 12447, 16325721, 46501166, 43776208, 16322212, 13643882, 12248982, 274550933, 114646366, 257075263, 275971120, 272170508, 763904, 977551, 9377522, 20352886, 9606552, 14433516, 184741501, 10678112, 26382928, 160634779, 13342, 40828015, 3363151, 51626700, 19956247, 271130493, 121010126, 3582061, 665453, 30207611, 6279162, 1469, 46919190, 788352, 1166101, 15626025, 38712031, 38529101, 6729282, 26283, 45699168, 12710492, 14090784, 754545, 90084013, 57743, 22240840, 228823344, 45933, 226703, 273129688, 273522379, 23381812, 14343621, 263901829, 32317477, 247470038, 804737, 15205547, 8866342, 14606550, 19258731, 11678812, 799682, 25511570, 31619861, 1037531, 25561137, 19035850, 13076722, 16041298, 9043, 14364327, 186649861, 13325382, 48188423, 1477481, 6292882, 36842688, 2255981, 47561730, 14231243, 16420657, 268494205, 268361103, 5660162, 246299452, 26552935, 251591169, 14844433, 38436112, 253000603, 15683697, 98016260, 14147974, 57143, 172176348, 22541531, 662473, 32069017, 105216182, 651103, 18526946, 17643108, 17198702, 15590446, 17431020, 268332181, 195209380, 255582954, 25002633, 61835446, 97559485, 12730, 15974761, 788947, 5170661, 690493, 16302724, 108218166, 675163, 7562772, 89985800, 16912263, 235865365, 37644620, 5790712, 21039855, 13148, 260504203, 7189872, 22916314, 195631622, 5433512, 13282032, 14905651, 38024627, 10270402, 17805185, 15700989, 148014268, 95476887, 36423, 14141553, 16491362, 12851192, 14683469, 243529488, 1746801, 115155776, 6171182, 10668, 6750322, 45823131, 1177041, 1066161, 19608323, 30100884, 755414, 13740, 2008761, 6209692, 6648842, 14067470, 5635482, 247504574, 15473976, 44439023, 15634588, 19377318, 19865091, 19140065, 20884676, 12454882, 222972711, 18949876, 7140432, 1117901, 14873096, 243700945, 15073476, 217497345, 43764707, 11724, 7852352, 17846095, 1995961, 14228114, 8315692, 10295382, 255935367, 7215612, 14564533, 7508092, 3174971, 792700, 767, 656823, 16677919, 67533248, 783772, 724063, 12299972, 18752733, 14787305, 12022942, 92088631, 5379862, 220226736, 15631379, 17243913, 3137231, 7789092, 6533132, 60558106, 8007362, 248381185, 156735510, 257736819, 257872871, 2059361, 2916601, 179023969, 1538151, 11587972, 26402409, 818992, 15826805, 3102231, 59593, 35623, 1557891, 46024962, 25968420, 13732012, 14828647, 8035592, 5558952, 3936, 761975, 801042, 15765143, 14697055, 5605262, 14308115, 2949, 4782771, 15850822, 13274152, 14819012, 52866725, 7125712, 216440383, 14902917, 7785002, 9371902, 1793401, 806790, 15774846, 42378039, 222886569, 37774772, 10447802, 41573, 245937883, 52343, 194330823, 29382439, 677873, 19747458, 1475531, 14987072, 248554969, 27917246, 14654485, 621503, 133387135, 5688252, 180817904, 14472933, 16053148, 15396684, 6899112, 2688101, 619383, 1234471, 11343052, 242697358, 30358034, 6098102, 8195912, 17626590, 15484730, 1421741, 231752606, 6754702, 528, 6935722, 92467892, 9237272, 14495632, 16354399, 20458935, 7626072, 3175761, 11614832, 10230112, 74945315, 18344738, 747, 58413, 13222032, 5723122, 765748, 1718381, 9319222, 16618171, 807648, 18594810, 5668862, 804064, 17303085, 14248784, 60685002, 15525530, 7457792, 51387260, 603233, 63337932, 14253084, 14299859, 11267672, 740603, 12705292, 1034161, 15394484, 22525008, 3692, 58976920, 2976491, 33571661, 9061132, 8610, 78453, 861201, 6630862, 750653, 41990192, 5103, 765488, 6822, 743033, 14869355, 7591562, 15155313, 8501542, 18060712, 818363, 5724602, 15284915, 803367, 18480433, 1636901, 49833, 614573, 130583593, 5783382, 6981492, 17806443, 21067835, 24263, 2401531, 758088, 17898531, 19838339, 21345771, 2796701, 1606131, 1546, 69676545, 18086594, 87500803, 223685596, 28973875, 47916953, 22811777, 7101542, 14193518, 801917, 48151970, 2011461, 86778502, 1318181, 1849731, 16519114, 773664, 14129326, 663353, 131285388, 992361, 60829918, 11113, 16245927, 107532513, 106903876, 15518831, 602673, 2211301, 771629, 10743292, 21804094, 809314, 29579856, 6634652, 14893547, 14977429, 1087481, 5858892, 17060123, 870561, 792738, 1162271, 14982872, 14358790, 772581, 800144, 5504, 7585092, 1666871, 4999, 137576023, 210473314, 774842, 1262121, 799948, 14128251, 5333392, 1552371, 16729156, 799847, 2593261, 12463, 1389861, 111483, 14582194, 62673608, 760, 804152, 125696029, 54913, 31281673, 13993522, 18434341, 99453649, 804325, 2662, 155368179, 14403468, 5744892, 1786951, 38093269, 15732349, 10990, 6882192, 638773, 47339867, 774964, 11807032, 1385401, 14062113, 665313, 2563081, 14102025, 1305941, 6043562, 22313854, 14398600, 15337750, 774850, 81904556, 82855999, 64678157, 34106642, 40462814, 21056065, 121790186, 104468715, 140821612, 36823, 2180111, 3310, 54498329, 12766, 5887072, 3104051, 777781, 188763, 908941, 16895001, 12606, 109023, 2426, 2764, 13117, 14126914, 11604, 11688, 2219031, 9928832, 964, 7337442, 30573], u'next_cursor_str': u'0'}
        for id in friend_ids['ids']:
            self.write("User #{0}…".format(id))
            self.flush()
            yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + .1)
            friend = yield self.twitter_request(
                "/friendships/update",
                post_args={"user_id": id, "retweets": "false"},
                access_token=self.current_user["access_token"])
            self.write("DETWEETED<br>")


        self.finish("We’re Done!")
        #loop through them


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/sign-in", SignInHandler),
    (r"/sign-out", SignOutHandler),
    (r"/bye-bye", ByeByeHandler),
], twitter_consumer_key="r9qhchd2GfIvENhaEbnBw", 
twitter_consumer_secret="DTs6nOJ2KxfaLcYwwQDZdZK47IC5gXY0Qs45O54Zuk",
cookie_secret="0E92HPEHRP64WZfWh6liJ3Xi16CYnEsTtvQqY9OH4IY=")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(int(options.on_port))
    tornado.ioloop.IOLoop.instance().start()



