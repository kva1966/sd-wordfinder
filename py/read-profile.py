from pstats import Stats

stats = Stats('profile.out')
stats.sort_stats('time')
stats.print_stats()
