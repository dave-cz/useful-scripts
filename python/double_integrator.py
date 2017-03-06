#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" skript mpc regulace """

import numpy as np
from cvxpy import Variable, sum_entries, Problem, Minimize, ECOS
import control
from time import time

# model matrices
A = np.matrix([[0, 1], [0, 0]])
B = np.matrix([[0, 0], [1, -1]])
C = np.matrix([[1, 0], [0, 1]])
D = np.matrix([[0, 0], [1, -1]])
Ts = 0.1
N = 20

sys_c = control.matlab.ss(A, B, C, D)
sys_d = control.matlab.c2d(sys_c, Ts, 'zoh')

n = A.shape[0]  # number of states
m = B.shape[1]  # number of inputs

# optimization variables
x = Variable(n, N+1)
u = Variable(m, N)

states = []

x0 = np.array([1, 0])
xf = np.array([0, 0])
u_max = 1

for t in xrange(N):
    cost = sum_entries(u[:, t])
    constr = [
        x[:, t+1] == sys_d.A * x[:, t] + sys_d.B * u[:, t],
        u[:, t] >= 0,
        u[:, t] <= u_max
    ]
    states.append(Problem(Minimize(cost), constr))

prob = sum(states)

prob.constraints.append(x[:, 0] == x0)
prob.constraints.append(x[:, N] == xf)

exec_start = time()
prob.solve(solver=ECOS)
exec_end = time()

print "status:", prob.status
print "value:", prob.value
print "solving time:", exec_end - exec_start, "s"

print "u[0] =", u[0, :].value
print "u[1] =", u[1, :].value
print "x[0] =", x[0, :].value
print "x[1] =", x[1, :].value
