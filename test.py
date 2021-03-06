#%%
import numpy as np
import datetime
import matplotlib.pyplot as plt
from training_classifier import Classifier as TrainingClassifier
from classifier import Classifier
import time
#%%

#%%
row_probs =  np.array([
    [0.79068811, 0.20931189], # [prob row 1 is target, prob row 1 is non-target]
    [0.95805819, 0.04194181], # [prob row 2 is target, prob row 2 is non-target]
    [0.87544911, 0.12455089], # etc.
    [0.7618169,  0.2381831 ],
    [0.69811839, 0.30188161],
    [0.88931632, 0.11068368]
])

print("ARGMAX OF:", row_probs[:, 1]) # [0.20931189 0.04194181 0.12455089 0.2381831  0.30188161 0.11068368]
pred_row = np.argmax(row_probs[:, 1])
print("PRED:", pred_row) # 4
#%%
# %%
# data =  [4164.103, 4168.718, 4164.103, 4134.872, 4142.051, 4168.205, 4160.0, 4160.855, 4161.709, 4162.564, 4162.564, 4167.692, 4171.026, 4174.359, 4172.308, 4169.231, 4174.359, 4179.487, 4182.564, 4182.051, 4182.051, 4189.231, 4188.718, 4192.821, 4191.282, 4189.744, 4193.846, 4196.923, 4198.462, 4199.487, 4197.949, 4203.077, 4204.615, 4196.41, 4196.41, 4203.077, 4197.179, 4191.282, 4195.385, 4196.41, 4203.077, 4185.128, 4155.385, 4174.359, 4196.923, 4194.359, 4169.231, 4138.974, 4156.923, 4179.487, 4187.179, 4164.615, 4127.692, 4158.974, 4167.179, 4156.923, 4140.513, 4124.103, 4147.179, 4170.256, 4164.615, 4157.436, 4150.256, 4162.564, 4172.821, 4163.59, 4164.103, 4172.308, 4172.308, 4172.308, 4175.897, 4175.897, 4178.718, 4181.538, 4181.026, 4184.103, 4185.128, 4193.846, 4194.872, 4189.231, 4191.282, 4193.846, 4195.897, 4197.949, 4200.0, 4202.051, 4205.641, 4205.066, 4204.49, 4203.915, 4203.34, 4202.764, 4202.189, 4201.614, 4201.038, 4200.463, 4199.887, 4199.312, 4198.737, 4198.161, 4197.586, 4197.011, 4196.435, 4195.86, 4195.285, 4194.709, 4194.134, 4193.558, 4192.983, 4192.408, 4191.832, 4191.257, 4190.682, 4190.106, 4189.531, 4188.956, 4188.38, 4187.805, 4187.23, 4186.654, 4186.079, 4185.503, 4184.928, 4184.353, 4183.777, 4183.202, 4182.627, 4182.051, 4174.359, 4173.846, 4173.333, 4179.487, 4181.538, 4186.667, 4186.154, 4185.128, 4186.154, 4188.205, 4197.436, 4194.872, 4189.744, 4194.872, 4200.0, 4201.795, 4203.59, 4201.538, 4198.462, 4200.0, 4202.564, 4195.897, 4195.385, 4196.41, 4197.436, 4181.538, 4165.641, 4174.872, 4189.231, 4185.128, 4178.462, 4141.538, 4147.692, 4167.179, 4181.538, 4184.103, 4111.282, 4146.923, 4182.564, 4190.769, 4166.154, 4154.359, 4142.564, 4174.872, 4156.41, 4165.128, 4173.846, 4169.231, 4164.615, 4166.154, 4170.256, 4177.949, 4177.436, 4178.974, 4180.513, 4182.564, 4187.692, 4186.667, 4185.641, 4193.846, 4197.436, 4198.462, 4193.333, 4192.308, 4203.077, 4198.718, 4194.359, 4197.949, 4204.103, 4194.872, 4186.154, 4192.051, 4197.949, 4205.641, 4184.103, 4181.026, 4177.949, 4180.769, 4183.59, 4165.641, 4135.385, 4162.564, 4169.744, 4174.872, 4160.0, 4118.462, 4151.795, 4152.821, 4153.846, 4160.513, 4141.538, 4160.0, 4173.333, 4155.385, 4159.487, 4169.231, 4169.231, 4170.769, 4171.282, 4176.154, 4181.026, 4182.051, 4184.615, 4182.051, 4182.564, 4190.256, 4188.718, 4191.282, 4193.846, 4195.897, 4202.051, 4197.436, 4196.923, 4204.615, 4205.128, 4197.692, 4190.256, 4197.436, 4190.256, 4196.923, 4194.872, 4177.436, 4186.154, 4183.077, 4181.538, 4166.923, 4152.308, 4165.641, 4158.462, 4157.436, 4161.538, 4142.051, 4168.205, 4149.231, 4131.795, 4138.718, 4145.641, 4150.769, 4169.231, 4156.41, 4157.949, 4164.615, 4169.744, 4174.359, 4169.744, 4171.282, 4179.487, 4181.026, 4185.128, 4183.846, 4182.564, 4190.256, 4192.308, 4192.821, 4193.333, 4194.359, 4202.564, 4198.974, 4195.385, 4198.462, 4205.641, 4198.974, 4189.231, 4197.949, 4200.0, 4202.051, 4191.795, 4190.0, 4188.205, 4171.795, 4160.0, 4166.41, 4172.821, 4180.513, 4151.282, 4159.487, 4167.692, 4151.795, 4164.615, 4150.769, 4136.923, 4162.051, 4143.59, 4149.744, 4170.769, 4155.385, 4157.436, 4167.692, 4171.282, 4174.359, 4171.795, 4172.821, 4176.41, 4175.385, 4183.077, 4185.641, 4183.077, 4187.436, 4191.795, 4192.821, 4195.385, 4197.436, 4199.487, 4197.949, 4196.41, 4201.026, 4206.154, 4196.923, 4187.692, 4197.436, 4191.795, 4193.846, 4190.769, 4165.128, 4176.923, 4179.487, 4175.385, 4159.744, 4144.103, 4171.282, 4161.026, 4138.974, 4161.538, 4152.308, 4166.154, 4153.846, 4132.821, 4164.615, 4162.564, 4168.718, 4174.872, 4166.667, 4165.641, 4168.974, 4172.308, 4175.897, 4175.822, 4175.747, 4175.672, 4175.597, 4175.522, 4175.447, 4175.372, 4175.297, 4175.222, 4175.147, 4175.072, 4174.997, 4174.922, 4174.847, 4174.772, 4174.697, 4174.622, 4174.547, 4174.472, 4174.396, 4174.321, 4174.246, 4174.171, 4174.096, 4174.021, 4173.946, 4173.871, 4173.796, 4173.721, 4173.646, 4173.571, 4173.496, 4173.421, 4173.346, 4173.271, 4173.196, 4173.121, 4173.046, 4172.971, 4172.896, 4172.821, 4193.846, 4193.59, 4193.333, 4194.872, 4202.051, 4201.538, 4193.846, 4196.923, 4200.0, 4195.385, 4198.974, 4187.949, 4176.923, 4187.179, 4173.333, 4174.872, 4173.846, 4148.205, 4169.744, 4166.667, 4163.59, 4168.205, 4129.231, 4158.462, 4160.0, 4137.949, 4162.564, 4162.564, 4162.564, 4163.333, 4164.103, 4166.154, 4170.256, 4171.795, 4180.513, 4180.513, 4180.513, 4184.615, 4188.205, 4188.205, 4188.205, 4190.256, 4202.051, 4201.026, 4197.949, 4198.974, 4196.923, 4194.872, 4192.821, 4198.462, 4194.872, 4193.077, 4191.282, 4173.333, 4184.615, 4182.051, 4179.487, 4168.718, 4144.615, 4172.821, 4160.513, 4162.564, 4164.615, 4163.846, 4163.077, 4155.385, 4132.308, 4162.051, 4156.41, 4160.513, 4173.333, 4167.179, 4173.333, 4178.462, 4176.41, 4178.462, 4180.513, 4181.538, 4184.615, 4191.026, 4197.436, 4195.641, 4193.846, 4198.974, 4199.487, 4198.462, 4202.564, 4208.718, 4194.359, 4181.026, 4196.41, 4207.692, 4211.282, 4178.718, 4146.154, 4162.564, 4178.974, 4168.462, 4157.949, 4141.538, 4175.897, 4147.692, 4151.795, 4165.641, 4129.744, 4146.41, 4163.077, 4149.744, 4165.128, 4164.872, 4164.615, 4177.949, 4169.744, 4171.282, 4172.821, 4182.564, 4186.667, 4187.692, 4188.718, 4193.846, 4192.308, 4192.564, 4192.821, 4196.923, 4206.154, 4207.179, 4198.462, 4191.282, 4200.513, 4196.923, 4186.667, 4191.538, 4196.41, 4181.795, 4167.179, 4134.872, 4169.744, 4185.641, 4198.974, 4153.333, 4106.154, 4140.256, 4174.359, 4175.385, 4152.821, 4120.0, 4162.051, 4165.641, 4151.282, 4174.872, 4172.821, 4173.846, 4174.872, 4174.615, 4174.359, 4175.897, 4184.615, 4193.846, 4187.179, 4187.179, 4191.795, 4193.333, 4200.0, 4199.231, 4198.462, 4201.026, 4209.231, 4195.128, 4181.026, 4197.436, 4196.923, 4191.538, 4186.154, 4151.795, 4168.205, 4171.026, 4173.846, 4165.128, 4141.026, 4148.205, 4155.385, 4126.667, 4164.615, 4156.667, 4148.718, 4166.154, 4144.615, 4158.974, 4171.795, 4171.282, 4173.333, 4168.205, 4173.333, 4175.385, 4177.436, 4184.103, 4184.103, 4187.051, 4190.0, 4192.949, 4195.897, 4200.0, 4197.436, 4200.769, 4204.103, 4199.487, 4189.744, 4202.564, 4197.436, 4183.59, 4195.897, 4166.154, 4157.436, 4183.59, 4185.128, 4186.154, 4141.026, 4133.333, 4170.769, 4173.333, 4175.897, 4135.897, 4117.949, 4168.718, 4159.487, 4156.923, 4173.333, 4164.103, 4167.692, 4171.795, 4175.897, 4184.615, 4179.487, 4182.051, 4188.205, 4185.641, 4190.256, 4190.769, 4191.282, 4197.436, 4196.41, 4198.205, 4200.0, 4202.051, 4199.487, 4197.949, 4196.41, 4190.769, 4202.051, 4179.487, 4148.205, 4175.897, 4176.923, 4173.333, 4169.744, 4144.615, 4169.744, 4162.051, 4154.359, 4161.538, 4120.513, 4145.897, 4171.282, 4148.718, 4165.641, 4167.949, 4170.256, 4176.923, 4172.308, 4173.846, 4175.385, 4180.0, 4190.256, 4187.179, 4188.205, 4190.769, 4193.333, 4195.897, 4198.462, 4194.359, 4201.538, 4204.103, 4197.436, 4193.846, 4205.128, 4188.205, 4177.949, 4195.385, 4183.077, 4185.641, 4167.692, 4151.282, 4171.282, 4153.846, 4172.308, 4165.128, 4137.949, 4167.692, 4137.436, 4155.641, 4173.846, 4149.744, 4155.385, 4155.8, 4156.215, 4156.63, 4157.045, 4157.46, 4157.875, 4158.291, 4158.706, 4159.121, 4159.536, 4159.951, 4160.366, 4160.781, 4161.197, 4161.612, 4162.027, 4162.442, 4162.857, 4163.272, 4163.687, 4164.103, 4164.518, 4164.933, 4165.348, 4165.763, 4166.178, 4166.593, 4167.009, 4167.424, 4167.839, 4168.254, 4168.669, 4169.084, 4169.499, 4169.915, 4170.33, 4170.745, 4171.16, 4171.575, 4171.99, 4172.405, 4172.821, 4185.128, 4171.795, 4176.923, 4152.308, 4170.256, 4167.179, 4148.205, 4171.282, 4162.821, 4154.359, 4170.769, 4132.821, 4156.41, 4165.128, 4169.487, 4173.846, 4171.282, 4168.718, 4175.385, 4176.41, 4177.949, 4179.487, 4182.051, 4192.821, 4188.718, 4188.205, 4191.282, 4194.359, 4206.667, 4203.077, 4200.513, 4197.949, 4209.231, 4203.077, 4184.615, 4196.41, 4200.0, 4203.59, 4172.308, 4141.026, 4164.103, 4181.538, 4174.872, 4167.692, 4141.026, 4176.923, 4147.179, 4100.513, 4155.385, 4172.308, 4169.231, 4158.974, 4143.59, 4144.265, 4144.941, 4145.616, 4146.291, 4146.967, 4147.642, 4148.318, 4148.993, 4149.669, 4150.344, 4151.019, 4151.695, 4152.37, 4153.046, 4153.721, 4154.396, 4155.072, 4155.747, 4156.423, 4157.098, 4157.774, 4158.449, 4159.124, 4159.8, 4160.475, 4161.151, 4161.826, 4162.502, 4163.177, 4163.852, 4164.528, 4165.203, 4165.879, 4166.554, 4167.23, 4167.905, 4168.58, 4169.256, 4169.931, 4170.607, 4171.282, 4198.462, 4198.462, 4189.231, 4191.795, 4196.41, 4190.769, 4195.897, 4174.359, 4152.821, 4177.949, 4173.333, 4185.128, 4156.41, 4130.256, 4163.59, 4169.744, 4175.897, 4139.487, 4111.795, 4138.205, 4164.615, 4157.436, 4172.308, 4172.186, 4172.063, 4171.941, 4171.819, 4171.697, 4171.575, 4171.453, 4171.331, 4171.209, 4171.087, 4170.965, 4170.842, 4170.72, 4170.598, 4170.476, 4170.354, 4170.232, 4170.11, 4169.988, 4169.866, 4169.744, 4169.621, 4169.499, 4169.377, 4169.255, 4169.133, 4169.011, 4168.889, 4168.767, 4168.645, 4168.523, 4168.4, 4168.278, 4168.156, 4168.034, 4167.912, 4167.79, 4167.668, 4167.546, 4167.424, 4167.302, 4167.179, 4162.564, 4171.795, 4181.026, 4186.667, 4155.385, 4142.051, 4170.256, 4142.051, 4160.513, 4141.795, 4123.077, 4160.0, 4164.615, 4154.872, 4165.641, 4158.974, 4169.744, 4178.462, 4173.333, 4174.615, 4175.897, 4182.051, 4188.718, 4187.692, 4186.667, 4190.256, 4193.846, 4194.103, 4194.359, 4197.949, 4205.128, 4206.667, 4196.41, 4194.359, 4205.641, 4192.308, 4187.179, 4200.513, 4206.154, 4201.026, 4145.641, 4160.769, 4175.897, 4195.897, 4197.949, 4128.718, 4091.282, 4138.974, 4186.667, 4179.487, 4139.487, 4154.359, 4169.231, 4162.564, 4151.795, 4160.256, 4168.718, 4166.667, 4169.744, 4178.205, 4186.667, 4186.154, 4187.179, 4188.974, 4190.769, 4191.282, 4189.744, 4194.872, 4209.231, 4204.103, 4194.872, 4200.256, 4205.641, 4196.41, 4190.256, 4201.026, 4187.692, 4187.949, 4188.205, 4171.795, 4184.615, 4159.487, 4154.359, 4156.667, 4158.974, 4171.795, 4140.513, 4130.769, 4162.051, 4161.795, 4161.538, 4152.308, 4143.077, 4160.513, 4165.641, 4166.667, 4174.359, 4168.718, 4171.282, 4177.436, 4180.0, 4187.179, 4185.641, 4184.615, 4190.769, 4193.333, 4195.897, 4195.385, 4194.872, 4203.59, 4203.59, 4197.436, 4192.821, 4205.128, 4197.949, 4187.179, 4195.385, 4175.385, 4177.436, 4172.308, 4167.179, 4176.923, 4156.41, 4162.564, 4162.414, 4162.264, 4162.114, 4161.964, 4161.814, 4161.664, 4161.513, 4161.363, 4161.213, 4161.063, 4160.913, 4160.763, 4160.613, 4160.463, 4160.313, 4160.163, 4160.013, 4159.862, 4159.712, 4159.562, 4159.412, 4159.262, 4159.112, 4158.962, 4158.812, 4158.662, 4158.512, 4158.361, 4158.211, 4158.061, 4157.911, 4157.761, 4157.611, 4157.461, 4157.311, 4157.161, 4157.011, 4156.861, 4156.71, 4156.56, 4156.41, 4190.256, 4191.795, 4166.923, 4142.051, 4126.154, 4174.872, 4194.359, 4195.897, 4126.154, 4110.769, 4180.0, 4163.59, 4168.205, 4172.821, 4172.821, 4172.821, 4172.821, 4176.41, 4178.718, 4181.026, 4183.077, 4192.308, 4192.564, 4192.821, 4190.256, 4196.41, 4201.026, 4205.641, 4200.513, 4201.026, 4209.744, 4210.256, 4204.615, 4204.615, 4204.615, 4204.615, 4190.0, 4175.385, 4189.744, 4205.128, 4209.744, 4182.051, 4174.359, 4166.667, 4179.231, 4191.795, 4167.179, 4114.359, 4143.077, 4171.795, 4167.949, 4164.103, 4160.256, 4156.41, 4168.718, 4156.41, 4162.179, 4167.949, 4173.718, 4179.487, 4177.436, 4181.538, 4185.128, 4188.718, 4192.308, 4189.744, 4190.513, 4191.282, 4192.051, 4192.821, 4199.487, 4206.154, 4205.128, 4204.103, 4200.0, 4199.487, 4198.974, 4198.462, 4193.846, 4189.231, 4204.359, 4219.487, 4172.821, 4130.256, 4167.692, 4178.462, 4169.231, 4160.0, 4131.795, 4168.205, 4155.897, 4150.085, 4144.274, 4138.462, 4154.872, 4171.282, 4158.974, 4172.308, 4174.359, 4169.744, 4175.385, 4176.41, 4178.974, 4182.564, 4183.077, 4185.128, 4184.103, 4190.769, 4194.615, 4198.462, 4206.667, 4204.103, 4198.462, 4206.667, 4213.333, 4198.974, 4197.692, 4196.41, 4195.128, 4193.846, 4200.513, 4190.256, 4192.821, 4188.205, 4181.538, 4188.718, 4171.795, 4154.872, 4175.385, 4173.846, 4180.0, 4123.077, 4149.231, 4175.385, 4187.179, 4179.487, 4161.795, 4144.103, 4166.667, 4157.436, 4171.795, 4191.282, 4174.872, 4171.795, 4177.692, 4183.59, 4186.667, 4183.59, 4183.59, 4189.231, 4194.872, 4204.103, 4201.795, 4199.487, 4203.59, 4210.256, 4207.692, 4199.487, 4206.667, 4198.974, 4198.205, 4197.436, 4197.436, 4200.513, 4183.59, 4169.744, 4184.103, 4173.846, 4184.615, 4169.744, 4136.923, 4165.128, 4167.949, 4170.769, 4166.667, 4119.487, 4147.179, 4174.872, 4159.487, 4173.333, 4172.821, 4172.308, 4183.077, 4178.974, 4175.385, 4171.795, 4183.077, 4195.385, 4191.795, 4191.282, 4194.359, 4197.436, 4205.641, 4199.487, 4203.333, 4207.179, 4212.308, 4201.538, 4193.846, 4205.128, 4198.462, 4185.641, 4196.41, 4208.205, 4190.513, 4172.821, 4147.179, 4148.205, 4149.231, 4150.256, 4151.282, 4152.308, 4176.923, 4136.923, 4152.564, 4168.205, 4152.308, 4167.692, 4159.487, 4151.282, 4181.026, 4167.179, 4164.615, 4175.385, 4174.359, 4175.897, 4177.949, 4187.179, 4195.385, 4186.154, 4183.077, 4187.179, 4192.308, 4201.538, 4201.355, 4201.172, 4200.989, 4200.806, 4200.623, 4200.44, 4200.256, 4200.073, 4199.89, 4199.707, 4199.524, 4199.341, 4199.158, 4198.974, 4198.791, 4198.608, 4198.425, 4198.242, 4198.059, 4197.875, 4197.692, 4197.509, 4197.326, 4197.143, 4196.96, 4196.777, 4196.593, 4196.41, 4196.227, 4196.044, 4195.861, 4195.678, 4195.495, 4195.311, 4195.128, 4194.945, 4194.762, 4194.579, 4194.396, 4194.212, 4194.029, 4193.846, 4164.615, 4169.744, 4174.103, 4178.462, 4173.846, 4176.41, 4181.795, 4187.179, 4188.205, 4183.59, 4188.718, 4189.231, 4191.795, 4196.41, 4197.949, 4200.0, 4201.795, 4203.59]
# buffer = [4154.359, 4161.026, 4158.462, 4162.308, 4166.154, 4168.205, 4164.103, 4167.692, 4173.846, 4183.077, 4178.462, 4177.436, 4176.41, 4175.385, 4179.487, 4182.051, 4180.513, 4186.154, 4186.154, 4189.744, 4192.308, 4189.231, 4195.897, 4195.385, 4194.872, 4198.462, 4200.0, 4207.179, 4202.051, 4198.462, 4197.436, 4196.41, 4193.846, 4201.538, 4194.359, 4190.256, 4200.0, 4196.923, 4187.179, 4192.308, 4197.949, 4188.205, 4178.462, 4155.385, 4171.795, 4187.179, 4181.026, 4174.359, 4167.692, 4161.282, 4154.872, 4163.846, 4172.821, 4140.0, 4150.256, 4168.205, 4170.769, 4153.333, 4123.59, 4149.231, 4166.667, 4158.462, 4160.0, 4156.154, 4152.308, 4161.538, 4151.795, 4148.718, 4157.436, 4157.436, 4156.41, 4155.897, 4155.385, 4168.718, 4174.359, 4170.513, 4166.667, 4177.949, 4184.615, 4180.0, 4175.385, 4185.641, 4182.051, 4184.615, 4187.179, 4184.615, 4190.256, 4189.231, 4191.795, 4195.385, 4188.205, 4193.333, 4198.462, 4198.462, 4199.487, 4196.41, 4204.103, 4205.128, 4195.897, 4196.41, 4196.923, 4198.462, 4206.154, 4199.487, 4175.897, 4182.051, 4203.59, 4213.846, 4194.359, 4145.128, 4142.564, 4184.872, 4227.179, 4193.333, 4120.0, 4112.308, 4177.436, 4223.59, 4195.385, 4145.385, 4095.385, 4164.615, 4216.41, 4169.487, 4122.564, 4095.897, 4158.462, 4185.128, 4168.205, 4140.513, 4131.795, 4157.949, 4162.051, 4163.59, 4165.128, 4158.974, 4156.923, 4163.333, 4169.744, 4155.897, 4165.299, 4174.701, 4184.103, 4177.949, 4171.282, 4175.385, 4176.41, 4184.615, 4186.667, 4185.897, 4185.128, 4188.718, 4191.282, 4189.744, 4184.615, 4195.897, 4199.487, 4195.385, 4193.846, 4193.333, 4205.641, 4206.667, 4192.308, 4198.205, 4204.103, 4195.641, 4187.179, 4196.923, 4201.026, 4197.949, 4193.846, 4201.026, 4198.974, 4183.846, 4168.718, 4191.282, 4204.103, 4191.282, 4145.641, 4160.513, 4175.385, 4210.256, 4193.333, 4157.436, 4121.538, 4165.641, 4184.615, 4162.308, 4140.0, 4102.051, 4151.282, 4188.718, 4180.0, 4142.051, 4128.205, 4156.41, 4160.0, 4152.821, 4156.068, 4159.316, 4162.564, 4166.154, 4169.744, 4167.179, 4173.333, 4172.821, 4172.308, 4177.949, 4174.359, 4173.846, 4177.436, 4181.026, 4184.615, 4177.949, 4185.128, 4188.205, 4189.231, 4187.949, 4186.667, 4196.923, 4198.462, 4197.436, 4198.974, 4196.41, 4204.615, 4199.231, 4193.846, 4199.487, 4203.077, 4194.359, 4192.308, 4195.128, 4197.949, 4194.615, 4191.282, 4190.256, 4193.846, 4180.0, 4179.487, 4178.205, 4176.923, 4176.41, 4162.564, 4162.051, 4170.256, 4163.077, 4169.231, 4155.385, 4143.077, 4158.462, 4170.769, 4183.077, 4137.436, 4112.308, 4159.487, 4169.744, 4162.735, 4155.726, 4148.718, 4156.41, 4164.615, 4163.59, 4163.59, 4162.564, 4163.077, 4168.205, 4173.333, 4168.718, 4171.795, 4177.949, 4184.103, 4180.513, 4173.333, 4178.974, 4186.154, 4185.128, 4184.103, 4180.513, 4194.872, 4192.051, 4189.231, 4191.795, 4192.821, 4196.667, 4200.513, 4198.462, 4198.974, 4194.872, 4201.538, 4207.692, 4194.359, 4187.179, 4196.923, 4200.0, 4195.385, 4195.385, 4192.308, 4188.974, 4185.641, 4174.872, 4180.0, 4180.513, 4181.026, 4176.923, 4161.538, 4166.667, 4164.103, 4171.795, 4169.744, 4144.103, 4159.487, 4160.0, 4152.991, 4145.983, 4138.974, 4160.513, 4156.923, 4135.385, 4153.846, 4162.051, 4162.051, 4161.538, 4156.41, 4160.513, 4167.692, 4164.615, 4165.128, 4168.205, 4168.718, 4171.026, 4173.333, 4173.333, 4179.487, 4179.487, 4183.59, 4184.615, 4185.128, 4187.692, 4184.103, 4187.692, 4191.282, 4185.641, 4191.282, 4197.949, 4201.538, 4197.949, 4193.846, 4203.59, 4204.103, 4200.0, 4195.897, 4196.923, 4197.949, 4196.923, 4196.41, 4193.846, 4198.974, 4188.462, 4177.949, 4177.179, 4176.41, 4177.949, 4180.0, 4175.897, 4173.846, 4150.256, 4155.385, 4166.667, 4160.513, 4152.564, 4144.615, 4144.615, 4152.308, 4160.0, 4167.692, 4144.615, 4126.667, 4148.974, 4171.282, 4165.128, 4153.333, 4153.333, 4164.103, 4164.615, 4165.128, 4172.308, 4169.231, 4169.231, 4178.974, 4176.923, 4175.385, 4178.462, 4175.897, 4182.051, 4186.154, 4185.641, 4184.615, 4188.974, 4193.333, 4191.282, 4186.667, 4194.872, 4196.923, 4199.487, 4197.949, 4201.282, 4204.615, 4203.59, 4194.872, 4198.462, 4202.051, 4191.795, 4194.359, 4199.487, 4196.41, 4189.231, 4182.051, 4176.923, 4188.718, 4188.974, 4189.231, 4166.667, 4149.744, 4166.154, 4168.718, 4161.795, 4154.872, 4136.923, 4173.846, 4155.897, 4143.077]

# clf = Classifier(time.time())
# clf.data = data
# clf.buffer = buffer
# clf.run_prediction()

# array of samples - data
# arr = np.array([
#     "e1_v1", "e1_v2", "e1_v3","e1_v4",
#     "e2_v1", "e2_v2", "e2_v3", "e2_v4"
# ])
# # array of epochs 
# new_arr = [
#     ["e1_v1", "e1_v2", "e1_v3", "e1_v4"], 
#     ["e2_v1", "e2_v2", "e2_v3", "e2_v4"]
# ]
# print("RUNNING")

# window = arr[1:] # ['e2_v2' 'e2_v3' 'e2_v4']
# final = np.concatenate((window, np.zeros(5)))
# print("FINAL:", final)
# new_arr.append(final)
# %%

# # %%
# clf = TrainingClassifier(time.time())
# clf.classify_training_data()
# #%%