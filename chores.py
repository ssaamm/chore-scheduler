#!/usr/bin/env python

# Chore assigner
# 
# Usage: python chores.py <chore file> [<num weeks>]
#
# Lines of a chore file can be in this format:
#
# <period (in weeks)> <init assignee> <description>
# or
# <extra assignee>

import collections
import sys

Chore = collections.namedtuple('Chore', ['period_wks', 'assignee', 'description'])
Week = collections.namedtuple('Week', ['num', 'chores'])

def assign(chore, assignees, week_num):
    init_assignee_ndx = assignees.index(chore.assignee)
    new_assignee = assignees[(init_assignee_ndx + week_num) % len(assignees)]
    return Chore(chore.period_wks, new_assignee, chore.description)

def get_chores(all_chores, assignees, week_num):
    return (assign(c, assignees, week_num)
            for c in all_chores if week_num % c.period_wks == 0)

if __name__ == '__main__':
    all_chores = []
    assignees = set()

    if len(sys.argv) < 2:
        print 'Usage: {} <chore file> [<num weeks>]'.format(sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        for line in f:
            s = line.split()
            if len(s) < 2:
                assignees.add(s[0])
            else:
                all_chores.append(Chore(period_wks=int(s[0]),
                    assignee=s[1],
                    description=' '.join(s[2:])))
                assignees.add(s[1])

    assignees = list(assignees)
    num_weeks = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    weeks = [Week(num=i, chores=get_chores(all_chores, assignees, i))
            for i in range(num_weeks)]

    max_assignee_len = max(len(s) for s in assignees)
    for week in weeks:
        print '## Week', week.num
        for chore in week.chores:
            print '[ ] {a:{awdth}} - {c}'.format(a=chore.assignee,
                    awdth=max_assignee_len + 1,
                    c=chore.description)
        print
