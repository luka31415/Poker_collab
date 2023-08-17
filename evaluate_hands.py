import random
import time

def RoyalFlush(cards, numbers, symbols):
    if numbers[9] > 0 and numbers[12] > 0:
        if StraightFlush(cards, numbers, symbols):
            return 9
    return 0

def StraightFlush(cards, numbers, symbols):
    straight = Straight(cards, numbers, symbols)
    flush = Flush(cards, numbers, symbols)
    if straight and flush:
        return straight + flush - 1
    return 0

def Flush(cards, numbers, symbols):
    for symbol in symbols:
        if symbol > 4:
            return 5 + HighCard(cards, numbers, symbols)
    return 0

def Straight(cards, numbers, symbols):
    breakLoop = False
    for i in range(0, 11):
        for j in range(0, 5):
            if not (i+j) % 13 in numbers:
                breakLoop = True
                break
        if not breakLoop:
            return 4 + (i + 4) / 13
        else:
            breakLoop = False
    return 0

def Pair(cards, numbers, symbols):
    if 2 in numbers:
        return 1 + numbers.index(2) / 13 + HighCard(cards, numbers, symbols) / 13
    return 0

def ThreeOfAKind(cards, numbers, symbols):
    if 3 in numbers:
        return 3 + numbers.index(3) / 13 + HighCard(cards, numbers, symbols) / 13
    return 0

def FourOfAKind(cards, numbers, symbols):
    if 4 in numbers:
        return 7 + numbers.index(4) / 13 + HighCard(cards, numbers, symbols) / 13
    return 0

def TwoPair(cards, numbers, symbols):
    if 2 in numbers:
        numbers2 = numbers.copy()
        numbers2.remove(2)
        if 2 in numbers2:
            return 2
    return 0

def FullHouse(cards, numbers, symbols):
    if 3 in numbers and 2 in numbers:
        return 6
    return 0

def HighCard(cards, numbers, symbols):
    return max(numbers)/13

def EvaluateCards(cards):
    funcs = [RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush, Straight, ThreeOfAKind, TwoPair, Pair, HighCard]
    symbols = [0] * 4
    numbers = [0] * 13
    for card in cards:
        numbers[card[1]-2] += 1
        symbols[card[0]-1] += 1
    score = 0
    for func in funcs:
        score += func(cards, numbers, symbols)
        if score != 0:
            return score

def GenerateHands(cards):
    hands = []
    for card1 in cards:
        copy = cards.copy()
        copy.remove(card1)
        for card2 in copy:
            if card2[1] >= card1[1] and card2[0] >= card1[0]:
                hands.append([card1, card2])
    return hands
            
def GenerateTable(cards, tableCards):
    table = tableCards.copy()
    copy = cards.copy()
    for i in range(5-len(tableCards)):
        table.append(random.choice(copy))
        copy.remove(table[-1])
    return table

def EvaluatePosition(cards, playerHand, tableCards, depth):
    hands = GenerateHands(cards)
    
    totalScore = 0
    
    for hand in hands:
        handScore = 0
        cardCopy = cards.copy()
        cardCopy.remove(hand[0])
        cardCopy.remove(hand[1])
        for i in range(depth):
            table = GenerateTable(cardCopy, tableCards)
            enemyCards = table.copy()
            enemyCards.extend(hand)
            playerCards = table.copy()
            playerCards.extend(playerHand)
            enemyScore = EvaluateCards(enemyCards)
            playerScore = EvaluateCards(playerCards)
            if playerScore > enemyScore:
                handScore += 1
            elif playerScore < enemyScore:
                handScore -= 1
            else:
                handScore += 0.1
        if handScore > 0:
            totalScore += 1
    totalScore /= len(hands) / 100
    return totalScore

def Main():
    times = []

    scores = []
    cards = []
    handCards = []
    for a in range(1, 5):
        for b in range (2, 15):
            if a < 3:
                handCards.append([a, b])
            cards.append([a,b])

    for card in handCards:
        time1 = time.time()
        for card2 in handCards:
            if card != card2:
                if card2[1] >= card[1] and card2[0] >= card[0]:
                    playerHand = [card, card2]
                    possibleCards = cards.copy()
                    possibleCards.remove(card)
                    possibleCards.remove(card2)
                    scores.append([playerHand, EvaluatePosition(possibleCards, playerHand, [], 9900)])
                    print(scores[-1])
        time2 = time.time()
        times.append(time2-time1)

    print(sum(times) / len(times))
    print(len(times))
    print(sum(times))

    with open("scores.txt", "w") as f:
        f.writelines(str(scores))
    
if __name__ == "__main__":
    Main()