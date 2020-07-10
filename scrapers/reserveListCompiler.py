
# this script compiles the value of all reserved list cards.
# It does this by searching a reserved list sql database,
# consulting the price chart for today,
# and pushing the sum of every reserved list card to an sql table called "reserved list sum"
# "reserved list sum" has two rows: date, and sum

# rlcompile = select cardid from cards where reservelist = true
# total_sum = 0
# for card in rlcompile:
#       rlcardprice = select price from prices where cardid=card and date = today
#       total_sum = total_sum + rlcardprice
# return total_sum

# write total_sum to "reserved list sum" along with date


# to-do #
# add a table called "reserved list sum" that has two values: date, and sum
# add a row to cards called "reserved list"
# write a script to update the reserved list value of all cards
# write a script to update the historical values in "reserved list sum"