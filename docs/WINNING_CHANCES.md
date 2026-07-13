# How to work out all the chances of winning on the UK National Lottery

#### [Euromillions, US Powerball and other Lottery Chances](https://www.kjartan.co.uk/games/lottodds.htm#others) 
## THE GAME

You select six numbers from 1–59. Six numbers are drawn plus a seventh "bonus ball".

### Approximate chances of matching the drawn numbers

| Result | Chance |
|----------|----------|
| JACKPOT (matching all six numbers) | 1 in 45 million |
| FIVE + THE BONUS BALL | 1 in 7.5 million |
| FIVE | 1 in 150,000 |
| FOUR | 1 in 2,000 |
| THREE | 1 in 100 |
| TWO | 1 in 10 |

### Other chances

| Event | Chance |
|---------|---------|
| Winning any prize* | 1 in 9.2 (nearly 11%) |
| Matching exactly one number | 1 in 2.5 (nearly 40%) |
| Matching no numbers | 1 in 2 (about 51%) |

\* You need to match two or more numbers to win a prize.

> If you buy one lottery ticket every minute for the next 86 years, the chances are that **one** ticket will win the UK lottery jackpot.

---


## How to calculate the different chances
### Step-by-Step Breakdown of the Calculation
The formula for combinations is:

$$
\binom{n}{r} = \frac{n!}{r!(n-r)!}
$$


Where:
* **\(n\)** is the total number of items to choose from (\(n = 59\))
* **\(r\)** is the number of items being chosen (\(r = 6\))
* **\(!\)** represents a factorial (multiplying a series of descending natural numbers)

Applying the values to the formula:
$$
^{59}C_6 = \frac{59!}{6!(59-6)!} = \frac{59!}{6! \times 53!}
$$
### Simplifying the Factorials

You can cancel out \(53!\) from both the top and the bottom of the fraction:
$$
^{59}C_6 = \frac{59 \times 58 \times 57 \times 56 \times 55 \times 54}{6 \times 5 \times 4 \times 3 \times 2 \times 1}
$$
Calculating the numerator:
$$
^{59}C_6 = \frac{32,441,381,280}{720} = 45,057,474
$$



### Jackpot chance

Only **one** of these ways will win you the jackpot.

Therefore:

```text
Jackpot chance = 1 in 45,057,474
```

or approximately **1 in 45 million**.

---

## Matching Three Numbers

We need to work out how many ways you can select six numbers so that three of them match and three do not.

Of the six numbers that are drawn, you need a combination of three.

<!-- IMAGE: C(6,3) = 20 -->

Your other three numbers must come from the 53 numbers that were not drawn.

<!-- IMAGE: C(53,3) = 23,426 -->

Multiply the answers together:

```text
20 × 23,426 = 468,520
```

Therefore there are **468,520** ways to match exactly three numbers.

```text
45,057,474 ÷ 468,520 = 96.167
```

So:

```text
Chance of matching 3 numbers = 1 in 96.167
```

or approximately:

```text
1 in 96
```
## 1. Choosing the 3 Winning Numbers

You need to select 3 numbers from the 6 that are actually drawn:

$$
^ {6}C_3  = \frac{6!}{3!\times3!} = 20
$$
or:
$$
\binom{6}{3} = \frac{6!}{3!\times3!} = 20
$$


[//]: # (^{59}C_6 = \frac{59!}{6!&#40;59-6&#41;!} = \frac{59!}{6! \times 53!})

## 2. Choosing the 3 Losing Numbers

The remaining 3 numbers in your set must come from the 53 numbers that were not drawn:

$$
^{53}C_3 = \frac{53!}{3!\times50!} = 23,426
$$
or: 
$$
\binom{53}{3} = \frac{53!}{3!\times50!} = 23,426
$$

## 3. Calculating the Final Chance

### Total Winning Combinations

Multiply the ways to get 3 winners by the ways to get 3 losers:

$$
20 \times 23,426 = 468,520
$$

### The Probability

Divide the total possible combinations by these winning combinations:

$$
\frac{45,057,474}{468,520} \approx 96.167
$$

Therefore, your chance of matching exactly 3 numbers is approximately:

$$
1 \text{ in } 96
$$

---

## Matching Four Numbers

We need:

- Four numbers from the six winners.
- Two numbers from the 53 losers.
### 1. Choosing the 4 Winning Numbers
this time we need to see how many ways there are of picking four numbers from the winning six, and then multiply this by how many ways there are of picking two numbers from the 53 losers.
$$
^6C_4\times^{53}C_2 = \frac{6!}{4!\times2!} \times \frac{53!}{2!\times51!} = 15 \times 1,378 = 20,670
$$

The result is:

```text
20,670 ways
```

Therefore: there are 20,670 ways of matching four winning numbers, your chances are 20,670 in 45,057,474. It works out that the chance of matching 4 numbers = 1 in 2,180
$$
\frac{45,057,474}{20,670} = 2179.848766
$$
```text
 or:
 ```
$$
\frac{45,057,474}{20,670} \approx 2,180
$$
```text
Chance of matching 4 numbers = 1 in 2,180
```

---

## Matching Five Numbers

This time we need to see how many ways there are of picking five numbers from the winning six, and then multiply this by how many ways there are of picking one number from the 53 losers. (This last bit's easy: if you have a choice of 53 things and you can choose one, how many choices have you got? 53 of course!)

Here comes the sums:

This means there are 318 ways of matching five winning numbers, but before we look at the chances, remember that with some of these ways your sixth number will also match the bonus number.

We need:

- Five numbers from the six winners.
- One number from the 53 losers.

$$
^6C_5\times^{53}C_1 = \frac{6!}{5!} \times \frac{53!}{1!} = 6 \times 53 = 318
$$

This gives:

```text
318 ways
```

However, some of these ways also match the bonus ball.

---

## Matching Five Numbers and the Bonus

Suppose you have matched five of the six main numbers.

One chosen number did not match.

There are 53 possible numbers remaining from which the bonus ball can be selected.

Therefore:

```text
Probability that the unmatched number is the bonus ball = 1/53
```

Since there are 318 combinations that match five numbers:

```text
(1/53) × 318 = 6
```

So:

```text
5 + Bonus combinations = 6
```

This leaves:

```text
318 − 6 = 312
```

combinations that match five numbers but not the bonus.

### Five Numbers (No Bonus)

```text
312 / 45,057,474
```

Therefore:

```text
Chance = 1 in 144,415
```

### Five Numbers Plus Bonus

```text
6 / 45,057,474
```

Therefore:

```text
Chance = 1 in 7,509,579
```

---

The odds of winning the UK National Lottery are:

```text
1 / 45,057,474
```

## Other Chances
### Winning Any Prize



## One quirky thought about the lottery

Assuming a life expectancy of 75 years, you can expect to be alive for roughly:

```text
40,000,000 minutes
```

Therefore your chance of dying in any particular minute is approximately:

```text
1 / 40,000,000
```

So if you want a lottery ticket, buy it in the last minute before the draw.

Otherwise you are more likely to die while waiting than to win the jackpot.

**Good luck!**

---

# The chances of other National Lottery Jackpots

When comparing lotteries, remember that odds alone do not determine value.

Ticket prices, jackpot sizes, rollover rules and lower-tier prizes all affect expected returns.

The table below compares only jackpot odds.

| Territory   | Game             | Jackpot Chance  | Highest Prize |
|-------------|------------------|-----------------|-------------|
| Poland      | Mini Lotto       | 1 / 850,668     | €700,000 |
| New Zealand | NZ Lotto         | 1 / 3,838,380   | NZ$44,000,000 |
| Sweden      | Swedish Lotto    | 1 / 6,724,520   | €25,600,000 |
| Austria     | Austrian Lotto   | 1 / 8,145,060   | €9,600,000 |
| Ireland     | Irish Lotto      | 1 / 10,737,573  | €19,000,000 |
| France      | French Lotto     | 1 / 19,068,840  | €23,900,000 |
| Spain       | Spanish Lotto    | 1 / 31,625,100  | €33,400,000 |
| UK          | National Lottery | 1 / 45,057,474  | £66,100,000 |
| Australia   | Powerball        | 1 / 134,490,400 | AU$107,000,000 |
| Europe      | EuroMillions     | 1 / 139,868,160 | €240,000,000 |
| USA         | Powerball        | 1 / 292,201,338 | $1,586,500,000 |
| Italy       | SuperEnaLotto    | 1 / 622,614,630 | €177,700,000 |
| Serbia      | Loto 7/39        | 1 / 15,380,937  | €7,700,000 |

---

# Summary of Numbers

| Numbers Matched | Number of Ways |
|----------------|---------------:|
| 6 | 1 |
| 5 + bonus | 6 |
| 5 | 312 |
| 4 | 20,670 |
| 3 | 468,520 |
| 2 | 4,392,375 |
| 1 | 17,218,110 |
| 0 | 22,957,480 |

| Total Ways |
|-----------:|
| 45,057,474 |

---

# Where does 45,057,474 come from?

The UK lottery asks you to choose six numbers from the numbers 1–59.

We need to calculate:

> How many different combinations of 6 numbers can be chosen from 59?

<!-- IMAGE: Combination notation C(59,6) -->

In mathematics this is written as:

<!-- IMAGE: nCr formula -->

To use the formula you need factorials.

A factorial is written using `!`:

```text
5! = 5 × 4 × 3 × 2 × 1 = 120
```

Expanding the formula gives:

```text
59! / (6! × 53!)
```

After cancellation and simplification:

```text
C(59,6) = 45,057,474
```

So there are:

```text
45,057,474
```

possible lottery selections, and only one wins the jackpot.

Therefore:

```text
Jackpot odds = 1 in 45,057,474
```