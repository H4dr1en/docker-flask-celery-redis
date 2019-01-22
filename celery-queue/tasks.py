import os
import time
from celery import Celery
import processing as proc
import requests, json

SERVER_GO_URL = 'http://serverauth:3030'
SERVER_DB_URL = 'http://serverdb:3031'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks.add')
def add(x, y):
    return x + y


@celery.task(name='tasks.process', bind=True, time_limit=60)
def process(self, req):

    self.update_state(state='PROGRESS', meta={
        "client": req['uid'],
        "output" : 'PROGRESS'
    })

    user = getUserSignatures(req['uid'])

    meta = { "client": req['uid'] }

    if(user is None):
        meta = {
            "client": req['uid'],
            "output" : 'FAILURE',
            "isAuthValid" : False,
            "msg" : "invalid user id"
        }

    else:

        try:
            meta["isAuthValid"] = proc.process(req, user)
            # meta["isAuthValid"] = proc_ml.process(req, user)
        except:
            meta = {
                "client": req['uid'],
                "output" : 'FAILURE',
                "isAuthValid" : False,
                "msg" : "Error while computing values",
            }

    try:
        requests.post(f'{SERVER_GO_URL}/authAnswer', data=json.dumps({
            "client": req['uid'],
            "isAuthValid": meta["isAuthValid"]
        }), headers={'Content-Type': 'application/json'})
        meta["output"] = "SUCCESS"

    except:
        meta = {
            "client": req['uid'],
            "output" : 'FAILURE',
            "isAuthValid": False,
            "msg": "communication with auth server failed"
        }

    finally:
        return meta


def getUserSignatures(uid):

    #res = requests.get(f'{SERVER_DB_URL}/user/id/{uid}')
    # return res.json()[0]["signatures"]

    return [
        {"uid":8,"abs":[2112,2032,2022,2022,2054,2078,2105,2137,2170,2206,2247,2306,2376,2463,2559,2661,2744,2820,2892,2978,3064,3135,3197,3234,3260,3279,3297,3318,3342,3382,3432,3484,3539,3595,3622,3636,3636,3636,3627,3614,3599,3879,4016,3993,4068,4151,4238,4298,4359,4424,4490,4549,4602,4633,4633,4601,4554,4499,4439,4367,4285,4197,4103,4048,4020,4045,4122,4234,4373,4518,4673,4816,4949,5065,5168,5262,5313,5337,5344,5350,5343,5326,5326,5338,5363,5384,5405,5427,5445,5464,5482,5494,5502,5502,5512,5527,5574,5640,5727,5834,5955,6083,6220,6364,6489,6587,6562,6536,6517,6517,6530,6544,6560,6582,6608,6642,6684,6731,6784,6841,6896,6949,6998,7047,7090,7128,7158,7193,7237,7285,7333,7381,7429,7484,7547,7614,7705,7811,7930,8038,8127,8207,8252,8269,8269,8242,8206,8161,8110,8060,8013,7985,7969,7969,7969,7989,8011,8035,8059,8085,8119,8161,8207,8256,8310,8364,8407,8444,8463,8476,8486,8486],"ords":[6588,6701,6736,6736,6751,6738,6676,6581,6452,6244,5983,5670,5303,4900,4481,4090,3718,3449,3225,3030,2922,2869,2852,2890,3031,3241,3554,3984,4491,5000,5467,5906,6254,6528,6754,6913,7022,7099,7142,7155,7149,4778,4142,4013,3856,3681,3599,3548,3517,3530,3580,3656,3780,3923,4078,4253,4417,4574,4638,4643,4609,4521,4379,4202,4048,3893,3753,3623,3556,3543,3565,3630,3743,3887,4037,4206,4388,4559,4698,4815,4815,4773,4704,4574,4411,4225,4043,3876,3719,3651,3626,3626,3668,3789,3966,4144,4303,4403,4470,4522,4562,4594,4632,4677,4727,4802,4750,4683,4659,4617,4557,4484,4381,4278,4178,4105,4048,4035,4070,4136,4241,4307,4348,4336,4298,4242,4198,4179,4179,4207,4273,4365,4429,4460,4468,4468,4458,4451,4469,4502,4560,4614,4666,4707,4753,4823,4906,4946,4956,4946,4900,4814,4701,4598,4514,4443,4398,4379,4379,4404,4458,4530,4567,4567,4550,4480,4386,4276,4203,4169,4162,4185],"time":[33681995,33682005,33682015,33682025,33682035,33682045,33682055,33682065,33682075,33682085,33682095,33682105,33682115,33682125,33682135,33682145,33682155,33682165,33682175,33682185,33682195,33682205,33682215,33682225,33682235,33682245,33682255,33682265,33682275,33682285,33682295,33682305,33682315,33682325,33682335,33682345,33682355,33682365,33682375,33682385,33682395,33682506,33682516,33682526,33682536,33682546,33682556,33682566,33682576,33682586,33682596,33682606,33682616,33682626,33682636,33682646,33682656,33682666,33682676,33682686,33682696,33682706,33682716,33682726,33682736,33682746,33682746,33682756,33682766,33682776,33682786,33682796,33682806,33682816,33682826,33682836,33682846,33682856,33682866,33682876,33682886,33682896,33682906,33682916,33682926,33682936,33682946,33682956,33682966,33682976,33682986,33682996,33683006,33683016,33683026,33683036,33683046,33683056,33683066,33683076,33683086,33683096,33683106,33683116,33683126,33683136,33683207,33683217,33683227,33683237,33683247,33683257,33683267,33683277,33683287,33683297,33683307,33683317,33683327,33683337,33683347,33683357,33683367,33683377,33683387,33683397,33683407,33683417,33683427,33683437,33683447,33683457,33683467,33683477,33683487,33683497,33683507,33683517,33683527,33683537,33683547,33683557,33683567,33683577,33683587,33683597,33683607,33683617,33683627,33683637,33683647,33683657,33683667,33683677,33683687,33683697,33683707,33683717,33683727,33683737,33683747,33683757,33683767,33683777,33683787,33683797,33683807,33683817,33683827,33683837,33683847,33683857]},
        {"uid":8,"abs":[2963,2889,2850,2826,2812,2812,2812,2812,2830,2852,2890,2937,2990,3048,3122,3204,3280,3358,3441,3528,3622,3724,3830,3929,4044,4170,4278,4365,4439,4511,4591,4675,4713,4732,4737,4730,4730,4730,4893,5031,5063,5110,5184,5271,5353,5436,5509,5574,5629,5672,5707,5722,5722,5706,5671,5630,5584,5530,5472,5412,5355,5302,5281,5281,5322,5392,5480,5585,5695,5813,5935,6044,6149,6252,6346,6425,6493,6559,6613,6658,6701,6748,6804,6864,6926,6971,7010,7046,7079,7104,7124,7138,7153,7169,7201,7257,7330,7407,7488,7570,7651,7735,7810,7905,7850,7817,7798,7782,7773,7780,7798,7822,7853,7895,7941,7985,8030,8072,8112,8146,8180,8214,8247,8279,8315,8353,8397,8443,8490,8531,8569,8603,8635,8666,8713,8766,8843,8934,9027,9115,9199,9263,9297,9310,9299,9274,9239,9187,9123,9052,8994,8954,8927,8916,8923,8942,8966,8993,9022,9052,9081,9109,9137,9157,9173,9186,9202,9222,9250,9285,9330,9373,9414,9449,9462],"ords":[5826,6002,6066,6123,6143,6143,6119,6042,5904,5725,5528,5262,4950,4600,4247,3892,3559,3286,3052,2896,2808,2765,2777,2881,3046,3337,3696,4100,4576,5049,5509,5961,6254,6481,6664,6706,6716,6706,4426,3975,3839,3759,3636,3538,3458,3395,3367,3367,3386,3442,3519,3615,3739,3882,4028,4166,4249,4298,4291,4235,4147,4026,3878,3712,3560,3415,3275,3169,3122,3114,3156,3254,3389,3546,3739,3957,4177,4391,4499,4539,4528,4465,4368,4232,4092,3968,3856,3756,3709,3697,3709,3772,3868,4001,4134,4266,4359,4416,4449,4457,4462,4462,4470,4483,4483,4478,4473,4418,4358,4296,4219,4156,4103,4085,4094,4120,4190,4269,4355,4401,4406,4385,4324,4263,4204,4178,4173,4203,4263,4344,4412,4446,4457,4440,4419,4393,4393,4398,4436,4494,4565,4621,4657,4679,4697,4718,4747,4780,4824,4863,4870,4857,4813,4732,4626,4522,4436,4361,4317,4302,4307,4354,4422,4505,4581,4614,4619,4586,4516,4422,4339,4280,4236,4210,4218],"time":[33707481,33707491,33707501,33707511,33707521,33707531,33707541,33707551,33707561,33707571,33707581,33707591,33707601,33707611,33707621,33707631,33707641,33707651,33707661,33707671,33707681,33707691,33707701,33707711,33707721,33707731,33707741,33707751,33707761,33707771,33707781,33707791,33707801,33707811,33707821,33707831,33707841,33707851,33707972,33707982,33707992,33708002,33708012,33708022,33708032,33708042,33708052,33708062,33708072,33708082,33708092,33708102,33708112,33708122,33708132,33708142,33708152,33708162,33708172,33708182,33708192,33708202,33708212,33708222,33708232,33708242,33708252,33708262,33708272,33708282,33708292,33708302,33708312,33708322,33708332,33708342,33708352,33708362,33708372,33708382,33708392,33708402,33708412,33708422,33708432,33708442,33708452,33708462,33708472,33708482,33708492,33708502,33708512,33708522,33708532,33708542,33708552,33708562,33708572,33708582,33708592,33708602,33708612,33708653,33708663,33708673,33708683,33708693,33708703,33708713,33708723,33708733,33708743,33708753,33708763,33708773,33708783,33708793,33708803,33708813,33708823,33708833,33708843,33708853,33708863,33708873,33708883,33708893,33708903,33708913,33708923,33708933,33708943,33708953,33708963,33708973,33708983,33708993,33709003,33709013,33709023,33709033,33709043,33709053,33709063,33709073,33709083,33709093,33709103,33709113,33709123,33709133,33709143,33709153,33709163,33709173,33709183,33709193,33709203,33709213,33709223,33709233,33709243,33709253,33709263,33709273,33709283,33709293,33709303,33709313,33709323,33709333,33709343,33709353,33709363]},
        {"uid":8,"abs":[3039,3008,2966,2948,2935,2924,2936,2951,2972,2999,3029,3062,3090,3115,3145,3179,3220,3277,3344,3406,3468,3530,3592,3654,3705,3749,3786,3820,3851,3889,3931,3993,4068,4175,4285,4377,4456,4523,4571,4606,4630,4639,4639,4639,4629,4768,4816,4837,4860,4875,4894,4922,4954,4993,5037,5087,5142,5199,5260,5307,5344,5364,5369,5369,5345,5309,5261,5200,5139,5077,5030,4999,4979,4979,4991,5030,5088,5174,5278,5395,5507,5612,5712,5804,5874,5928,5973,6007,6034,6034,6034,6034,6034,6024,6009,6004,6004,6004,6020,6041,6062,6082,6112,6146,6202,6271,6356,6434,6508,6586,6668,6756,6855,6960,7060,7160,7259,7344,7401,7439,7453,7448,7429,7385,7337,7285,7254,7226,7205,7189,7179,7173,7173,7173,7186,7208,7237,7269,7307,7353,7401,7448,7479,7500,7519,7532,7541,7550,7561,7575,7591,7622,7663,7710,7761,7820,7883,7955,8031,8125,8236,8358,8477,8566,8636,8661,8666,8658,8644,8608,8557,8497,8442,8391,8350,8311,8277,8262,8262,8286,8315,8362,8420,8480,8541,8603,8667,8733,8844,8964,9089,9195,9286],"ords":[7026,7208,7241,7241,7219,7219,7186,7136,7077,6974,6841,6664,6429,6156,5886,5591,5280,4942,4702,4528,4369,4239,4128,4078,4065,4077,4139,4265,4435,4644,4909,5211,5581,5922,6244,6569,6815,7008,7139,7247,7340,7388,7406,7406,7390,5277,4971,4847,4723,4623,4540,4467,4405,4351,4317,4310,4321,4364,4431,4515,4611,4721,4840,4947,5024,5080,5106,5106,5078,5022,4941,4844,4725,4606,4487,4367,4275,4201,4176,4194,4241,4319,4409,4508,4609,4724,4849,4943,4984,4991,4976,4926,4854,4722,4585,4440,4288,4132,4027,3971,3948,3948,4004,4090,4247,4414,4588,4693,4771,4831,4876,4907,4929,4945,4957,4962,4962,4962,4951,4945,4940,4940,4940,4952,4959,4965,4956,4931,4895,4848,4781,4701,4616,4539,4468,4416,4400,4409,4462,4532,4614,4673,4690,4678,4657,4621,4576,4533,4516,4516,4535,4574,4628,4664,4677,4677,4641,4597,4546,4523,4530,4556,4609,4661,4713,4756,4802,4849,4867,4867,4851,4829,4797,4758,4699,4628,4547,4474,4427,4396,4396,4430,4482,4542,4602,4629,4636,4596,4510,4394,4270,4197,4158],"time":[74811553,74811563,74811573,74811583,74811593,74811603,74811613,74811623,74811633,74811643,74811653,74811663,74811673,74811683,74811693,74811703,74811713,74811723,74811733,74811743,74811753,74811763,74811773,74811783,74811793,74811803,74811813,74811823,74811833,74811843,74811853,74811863,74811873,74811883,74811893,74811903,74811913,74811923,74811933,74811943,74811953,74811963,74811973,74811983,74811993,74812124,74812134,74812144,74812154,74812164,74812174,74812184,74812194,74812204,74812214,74812224,74812234,74812244,74812254,74812264,74812274,74812284,74812294,74812304,74812314,74812324,74812334,74812344,74812354,74812364,74812374,74812384,74812394,74812404,74812414,74812424,74812434,74812444,74812454,74812464,74812474,74812484,74812494,74812504,74812514,74812524,74812534,74812544,74812554,74812564,74812574,74812584,74812594,74812604,74812614,74812624,74812634,74812644,74812654,74812664,74812674,74812684,74812694,74812704,74812714,74812724,74812734,74812744,74812754,74812764,74812774,74812784,74812794,74812804,74812814,74812824,74812834,74812844,74812854,74812864,74812874,74812884,74812894,74812904,74812914,74812924,74812934,74812944,74812954,74812964,74812974,74812984,74812994,74813004,74813014,74813024,74813034,74813044,74813054,74813064,74813074,74813084,74813094,74813104,74813114,74813124,74813134,74813144,74813154,74813164,74813174,74813184,74813194,74813204,74813214,74813224,74813234,74813244,74813254,74813264,74813274,74813284,74813294,74813304,74813314,74813324,74813334,74813344,74813354,74813364,74813374,74813384,74813394,74813404,74813414,74813424,74813434,74813444,74813454,74813464,74813474,74813484,74813494,74813504,74813514,74813524,74813534,74813544,74813554,74813564,74813574,74813584,74813586]},
        {"uid":8,"abs":[2739,2743,2732,2718,2718,2732,2745,2758,2778,2799,2823,2843,2859,2888,2922,2975,3040,3106,3170,3227,3278,3330,3387,3452,3533,3624,3724,3821,3917,4020,4124,4193,4238,4268,4286,4295,4300,4300,4300,4300,4300,4315,4538,4574,4596,4629,4675,4722,4773,4817,4858,4898,4935,4971,5002,5022,5035,5026,4999,4961,4919,4877,4835,4793,4752,4712,4684,4662,4653,4668,4698,4754,4824,4903,4989,5089,5197,5297,5372,5429,5464,5482,5488,5493,5493,5484,5490,5498,5511,5526,5544,5565,5588,5612,5636,5657,5676,5695,5715,5739,5780,5833,5889,5959,6038,6128,6230,6339,6440,6530,6612,6670,6701,6715,6703,6669,6620,6569,6521,6490,6469,6457,6447,6447,6459,6483,6517,6560,6608,6657,6707,6756,6803,6839,6868,6889,6907,6922,6941,6961,6985,7014,7058,7110,7160,7216,7286,7364,7450,7539,7636,7741,7847,7953,8022,8067,8079,8070,8046,8010,7963,7909,7860,7816,7783,7755,7734,7720,7726,7745,7775,7805,7850,7903,7949,7999,8053,8108,8185,8277,8399,8490,8560],"ords":[6485,6593,6645,6658,6644,6606,6519,6400,6253,6053,5817,5560,5259,4928,4594,4288,4001,3746,3569,3444,3356,3322,3322,3397,3548,3752,4037,4374,4747,5148,5527,5891,6114,6296,6450,6577,6659,6711,6735,6741,6734,6700,4675,4311,4137,3997,3881,3781,3709,3656,3633,3633,3647,3683,3740,3811,3891,3977,4068,4151,4211,4255,4270,4262,4239,4197,4131,4049,3954,3854,3746,3663,3597,3561,3556,3572,3626,3702,3794,3884,3982,4086,4182,4217,4212,4197,4144,4066,3964,3844,3712,3601,3508,3426,3387,3379,3392,3447,3535,3646,3764,3871,3947,4007,4056,4089,4112,4134,4155,4176,4195,4211,4221,4221,4221,4209,4192,4161,4120,4076,4028,3960,3881,3785,3706,3639,3604,3604,3624,3679,3754,3843,3901,3926,3926,3910,3873,3824,3779,3758,3752,3767,3807,3864,3895,3907,3907,3886,3865,3846,3854,3878,3936,4000,4067,4115,4162,4205,4249,4269,4274,4251,4226,4185,4134,4070,4004,3933,3881,3842,3821,3829,3856,3911,3971,4034,4069,4069,4039,3984,3892,3776,3685],"time":[74815238,74815248,74815258,74815268,74815278,74815288,74815298,74815308,74815318,74815328,74815338,74815348,74815358,74815368,74815378,74815388,74815398,74815408,74815418,74815428,74815438,74815448,74815458,74815468,74815478,74815488,74815498,74815508,74815518,74815528,74815538,74815548,74815558,74815568,74815578,74815588,74815598,74815608,74815618,74815628,74815638,74815648,74815749,74815759,74815769,74815779,74815789,74815799,74815809,74815819,74815829,74815839,74815849,74815859,74815869,74815879,74815889,74815899,74815909,74815919,74815929,74815939,74815949,74815959,74815969,74815979,74815989,74815999,74816009,74816019,74816029,74816039,74816049,74816059,74816069,74816079,74816089,74816099,74816109,74816119,74816129,74816139,74816149,74816159,74816169,74816179,74816189,74816199,74816209,74816219,74816229,74816239,74816249,74816259,74816269,74816279,74816289,74816299,74816309,74816319,74816329,74816339,74816349,74816359,74816369,74816379,74816389,74816399,74816409,74816419,74816429,74816439,74816449,74816459,74816469,74816479,74816490,74816500,74816510,74816520,74816530,74816540,74816550,74816560,74816570,74816580,74816590,74816600,74816610,74816620,74816630,74816640,74816650,74816660,74816670,74816680,74816690,74816700,74816710,74816720,74816730,74816740,74816750,74816760,74816770,74816780,74816790,74816800,74816810,74816820,74816830,74816840,74816850,74816860,74816870,74816880,74816890,74816900,74816910,74816920,74816930,74816940,74816950,74816960,74816970,74816980,74816990,74817000,74817010,74817020,74817030,74817040,74817050,74817060,74817070,74817080,74817090,74817100,74817110,74817120,74817130,74817140,74817150]},
        {"uid":8,"abs":[3008,2944,2902,2884,2884,2893,2907,2933,2970,3013,3058,3102,3128,3143,3158,3197,3253,3334,3415,3493,3563,3629,3700,3768,3837,3907,4012,4144,4295,4441,4578,4708,4814,4884,4930,4952,4952,4930,4896,4839,4875,4892,4928,4976,5018,5062,5112,5168,5227,5285,5340,5393,5437,5471,5498,5505,5491,5462,5419,5358,5286,5203,5122,5048,4998,4963,4963,4994,5048,5130,5244,5378,5523,5670,5815,5957,6060,6145,6217,6268,6294,6304,6294,6284,6276,6269,6262,6257,6257,6257,6257,6274,6283,6283,6293,6300,6324,6360,6421,6497,6584,6685,6801,6927,7042,7159,7282,7384,7472,7526,7546,7546,7524,7494,7456,7411,7368,7330,7295,7263,7236,7230,7237,7266,7301,7338,7373,7413,7457,7510,7571,7629,7683,7737,7789,7834,7875,7917,7962,8012,8070,8126,8181,8242,8309,8389,8479,8579,8685,8792,8901,8979,9035,9064,9070,9061,9039,9000,8950,8888,8833,8782,8743,8710,8698,8698,8720,8746,8789,8840,8911,8985,9066,9164,9274,9407,9523,9628],"ords":[6785,7083,7173,7242,7258,7237,7192,7079,6907,6697,6447,6117,5735,5342,4932,4512,4202,3958,3758,3643,3601,3609,3694,3899,4183,4566,5030,5548,6030,6450,6828,7113,7338,7522,7663,7746,7790,7811,7787,5211,4737,4575,4435,4292,4149,4043,3961,3906,3885,3885,3920,3981,4059,4167,4305,4462,4599,4713,4811,4856,4856,4826,4751,4658,4553,4417,4272,4121,3993,3894,3814,3792,3827,3899,4011,4131,4257,4410,4563,4717,4857,4899,4876,4837,4744,4616,4457,4286,4106,3950,3834,3745,3722,3733,3768,3868,4003,4162,4335,4458,4549,4608,4646,4669,4685,4700,4718,4739,4762,4784,4792,4792,4792,4800,4776,4733,4675,4612,4534,4447,4349,4251,4174,4112,4081,4075,4085,4127,4188,4263,4324,4355,4367,4353,4325,4288,4260,4253,4259,4290,4329,4373,4387,4379,4357,4327,4310,4303,4334,4391,4466,4531,4595,4657,4716,4753,4775,4765,4737,4698,4648,4574,4483,4385,4288,4231,4199,4199,4231,4288,4376,4465,4554,4583,4576,4546,4489,4430],"time":[74818443,74818453,74818463,74818473,74818483,74818493,74818503,74818513,74818523,74818533,74818543,74818553,74818563,74818573,74818583,74818593,74818603,74818613,74818623,74818633,74818643,74818653,74818663,74818673,74818683,74818693,74818703,74818713,74818723,74818733,74818743,74818753,74818763,74818773,74818783,74818793,74818803,74818813,74818823,74818933,74818943,74818953,74818963,74818973,74818983,74818993,74819003,74819013,74819023,74819033,74819043,74819053,74819063,74819073,74819083,74819093,74819103,74819113,74819123,74819133,74819143,74819153,74819163,74819173,74819183,74819193,74819203,74819213,74819223,74819233,74819243,74819253,74819263,74819273,74819283,74819293,74819303,74819313,74819323,74819333,74819343,74819353,74819363,74819373,74819383,74819393,74819403,74819413,74819423,74819433,74819443,74819453,74819463,74819473,74819483,74819493,74819503,74819513,74819523,74819533,74819543,74819553,74819563,74819573,74819583,74819593,74819603,74819613,74819623,74819633,74819643,74819653,74819663,74819673,74819683,74819693,74819703,74819713,74819723,74819733,74819743,74819753,74819763,74819773,74819783,74819793,74819803,74819813,74819823,74819833,74819843,74819853,74819863,74819873,74819883,74819893,74819903,74819913,74819923,74819933,74819943,74819953,74819963,74819973,74819983,74819993,74820003,74820013,74820023,74820033,74820043,74820053,74820063,74820073,74820083,74820093,74820103,74820113,74820123,74820133,74820143,74820153,74820163,74820173,74820183,74820193,74820203,74820213,74820215,74820225,74820235,74820245,74820255,74820265,74820275,74820285,74820295,74820305]},
        {"uid":8,"abs":[2301,2277,2254,2254,2254,2266,2286,2316,2353,2396,2444,2485,2522,2560,2603,2672,2756,2849,2945,3046,3144,3228,3302,3377,3444,3506,3577,3670,3778,3876,3974,4072,4155,4228,4286,4314,4323,4323,4323,4312,4299,4280,4235,4235,4235,4235,4278,4324,4372,4424,4485,4556,4628,4700,4777,4836,4883,4917,4932,4932,4918,4888,4847,4804,4751,4691,4635,4581,4549,4529,4529,4546,4582,4647,4738,4847,4963,5083,5218,5361,5489,5599,5696,5769,5823,5865,5896,5908,5908,5908,5908,5916,5921,5927,5934,5947,5961,5976,5990,6006,6022,6055,6092,6152,6227,6321,6417,6520,6628,6745,6869,6970,7055,7127,7169,7191,7180,7154,7154,7022,6968,6922,6881,6848,6818,6804,6804,6815,6846,6888,6929,6975,7031,7093,7176,7272,7356,7422,7476,7515,7551,7584,7620,7662,7716,7778,7851,7929,8001,8068,8143,8226,8326,8436,8546,8656,8766,8861,8946,8979,8979,8958,8918,8862,8796,8722,8651,8597,8554,8518,8487,8482,8493,8522,8553,8599,8653,8711,8769,8825,8880,8946,9012,9076,9138,9195,9249],"ords":[6530,6653,6681,6681,6657,6614,6511,6366,6193,5985,5741,5473,5162,4840,4511,4235,3994,3777,3626,3534,3481,3481,3539,3633,3803,4041,4325,4668,5057,5477,5852,6162,6429,6667,6832,6948,7009,7037,7043,7043,6993,6917,5187,4686,4502,4363,4200,4062,3942,3848,3791,3760,3768,3807,3867,3941,4031,4131,4260,4388,4516,4612,4672,4709,4724,4710,4676,4612,4542,4432,4297,4160,4031,3908,3803,3733,3686,3686,3721,3789,3891,3993,4093,4210,4339,4468,4537,4567,4567,4528,4465,4353,4220,4072,3943,3829,3725,3680,3665,3671,3721,3819,3949,4083,4198,4300,4369,4417,4450,4478,4505,4533,4562,4593,4616,4622,4616,4602,4602,4516,4468,4413,4346,4266,4178,4090,4005,3945,3901,3883,3894,3924,3982,4055,4138,4196,4223,4230,4208,4173,4129,4094,4080,4080,4107,4151,4206,4246,4254,4240,4214,4187,4162,4139,4197,4252,4316,4388,4446,4487,4517,4545,4560,4567,4562,4552,4530,4499,4443,4370,4289,4234,4196,4175,4175,4200,4245,4297,4354,4380,4365,4323,4234,4148,4065,4005,3991],"time":[74821737,74821747,74821757,74821767,74821777,74821787,74821797,74821807,74821817,74821827,74821837,74821847,74821857,74821867,74821877,74821887,74821897,74821907,74821917,74821927,74821937,74821947,74821957,74821967,74821977,74821987,74821997,74822007,74822017,74822027,74822037,74822047,74822057,74822067,74822077,74822087,74822097,74822107,74822117,74822127,74822137,74822147,74822228,74822238,74822248,74822258,74822268,74822278,74822288,74822298,74822308,74822318,74822328,74822338,74822348,74822358,74822368,74822378,74822388,74822398,74822408,74822418,74822428,74822438,74822448,74822458,74822468,74822478,74822488,74822498,74822508,74822518,74822528,74822538,74822548,74822558,74822568,74822578,74822589,74822599,74822609,74822619,74822629,74822639,74822649,74822659,74822669,74822679,74822689,74822699,74822709,74822719,74822729,74822739,74822749,74822759,74822769,74822779,74822789,74822799,74822809,74822819,74822829,74822839,74822849,74822859,74822869,74822879,74822889,74822899,74822909,74822919,74822929,74822939,74822949,74822959,74822969,74822979,74822989,74822999,74823009,74823019,74823029,74823039,74823049,74823059,74823069,74823079,74823089,74823099,74823109,74823119,74823129,74823139,74823149,74823159,74823169,74823179,74823189,74823199,74823209,74823219,74823229,74823239,74823249,74823259,74823269,74823279,74823289,74823299,74823309,74823319,74823329,74823339,74823349,74823359,74823369,74823379,74823389,74823399,74823409,74823419,74823429,74823439,74823449,74823459,74823469,74823479,74823489,74823499,74823509,74823519,74823529,74823539,74823549,74823559,74823569,74823579,74823589,74823599,74823609,74823619,74823629,74823639,74823649,74823659,74823669]},
        {"uid":8,"abs":[2742,2690,2657,2615,2615,2610,2618,2632,2659,2696,2732,2768,2808,2852,2896,2940,2981,3021,3071,3122,3164,3199,3228,3256,3283,3321,3363,3411,3489,3587,3721,3840,3950,4057,4162,4246,4317,4358,4381,4392,4392,4386,4349,4411,4446,4483,4525,4570,4622,4682,4746,4813,4870,4919,4959,4984,4999,4999,4986,4969,4939,4900,4855,4798,4734,4665,4619,4598,4593,4618,4673,4749,4841,4951,5073,5211,5341,5465,5575,5670,5756,5825,5871,5902,5920,5925,5920,5920,5915,5915,5905,5897,5897,5905,5920,5939,5961,5983,6006,6043,6089,6150,6228,6317,6402,6494,6601,6715,6837,6931,7007,7064,7094,7106,7096,7071,7035,6992,6952,6920,6902,6894,6887,6887,6887,6908,6941,6983,7023,7064,7108,7155,7204,7240,7267,7293,7320,7349,7378,7413,7451,7495,7548,7603,7659,7716,7783,7857,7948,8044,8149,8263,8379,8489,8573,8643,8682,8691,8679,8656,8617,8568,8514,8463,8427,8399,8386,8378,8378,8392,8414,8444,8478,8512,8548,8580,8609,8640,8670,8725,8797,8890,8985,9059],"ords":[6957,7059,7094,7133,7126,7086,7005,6875,6713,6497,6206,5866,5532,5145,4724,4397,4056,3705,3495,3300,3115,3015,2975,2975,3022,3158,3353,3586,3895,4256,4668,5088,5514,5912,6241,6524,6727,6874,6983,7044,7072,7077,4018,3604,3465,3325,3207,3105,3039,3000,2980,2987,3027,3088,3167,3277,3407,3548,3689,3830,3916,3959,3973,3953,3885,3786,3657,3527,3397,3254,3121,3019,2934,2890,2890,2918,2988,3079,3183,3298,3413,3538,3670,3798,3853,3859,3847,3784,3686,3565,3427,3278,3125,2997,2887,2823,2807,2823,2878,2976,3103,3249,3359,3446,3493,3524,3544,3564,3584,3605,3625,3646,3666,3672,3678,3684,3684,3678,3654,3617,3571,3504,3423,3329,3246,3171,3137,3129,3139,3171,3222,3286,3336,3353,3348,3319,3280,3235,3208,3203,3213,3255,3310,3373,3414,3428,3428,3396,3368,3358,3358,3397,3448,3511,3562,3610,3651,3681,3705,3726,3726,3719,3704,3685,3650,3604,3531,3456,3381,3329,3291,3276,3260,3306,3394,3459,3518,3573,3581,3553,3500,3421,3336,3248],"time":[74828657,74828667,74828677,74828687,74828697,74828707,74828717,74828727,74828737,74828747,74828757,74828767,74828777,74828787,74828797,74828807,74828817,74828827,74828837,74828847,74828857,74828867,74828877,74828887,74828897,74828907,74828917,74828927,74828937,74828947,74828957,74828967,74828977,74828987,74828997,74829007,74829017,74829027,74829037,74829047,74829057,74829067,74829218,74829228,74829238,74829248,74829258,74829268,74829278,74829288,74829298,74829308,74829318,74829328,74829338,74829348,74829358,74829368,74829378,74829388,74829398,74829408,74829418,74829428,74829438,74829448,74829458,74829468,74829478,74829488,74829498,74829508,74829518,74829528,74829538,74829548,74829558,74829568,74829578,74829588,74829598,74829608,74829618,74829628,74829638,74829648,74829658,74829668,74829678,74829688,74829698,74829708,74829718,74829728,74829738,74829748,74829758,74829768,74829778,74829788,74829798,74829808,74829818,74829828,74829838,74829848,74829858,74829868,74829878,74829888,74829898,74829908,74829918,74829928,74829938,74829948,74829958,74829968,74829978,74829988,74829998,74830008,74830018,74830028,74830038,74830048,74830058,74830068,74830078,74830088,74830098,74830108,74830118,74830128,74830138,74830148,74830158,74830168,74830178,74830188,74830198,74830208,74830218,74830228,74830238,74830248,74830258,74830268,74830278,74830288,74830298,74830300,74830310,74830320,74830330,74830340,74830350,74830360,74830370,74830380,74830390,74830400,74830410,74830420,74830430,74830440,74830450,74830460,74830470,74830480,74830490,74830500,74830510,74830520,74830530,74830540,74830550,74830560,74830570,74830580,74830590,74830600,74830610,74830620]}

    ]