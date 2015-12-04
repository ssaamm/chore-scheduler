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
from datetime import date, timedelta, datetime

DAYS_IN_WK = 7
SATURDAY = 5

DATE_FMT = '%Y-%m-%d'

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
        print 'Usage: {} <chore file> [<num weeks>] [<start date>]'.format(sys.argv[0])
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

    # http://stackoverflow.com/questions/16769902/
    start = date.today()
    if len(sys.argv) > 3:
        start = datetime.strptime(sys.argv[3], DATE_FMT)
    this_week = start + timedelta((DAYS_IN_WK + SATURDAY -
        start.weekday()) % DAYS_IN_WK)

    max_assignee_len = max(len(s) for s in assignees)
    for week in weeks:
        pretty_date = (this_week + timedelta(weeks=week.num)).strftime(DATE_FMT)
        print '## Week {wn} (ending {date})'.format(wn=week.num,
                date=pretty_date)
        for chore in week.chores:
            print '[ ] {a:{awdth}} - {c}'.format(a=chore.assignee,
                    awdth=max_assignee_len,
                    c=chore.description)
        print
