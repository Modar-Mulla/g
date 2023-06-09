import random
import os


steps = 6
tasks = 26
time = []
link = []
shift = []
is_visited = []

for i in range(27) :
    time.append(0)
    link.append([])
    is_visited.append(False)


#remove old solutions
if os.path.isfile("/home/rgalion211/g/playground/static/playground/files/all_results_steps.txt") :
    os.remove("/home/rgalion211/g/playground/static/playground/files/all_results_steps.txt")

if os.path.isfile("/home/rgalion211/g/playground/static/playground/files/optimal_result_steps.txt") :
    os.remove("/home/rgalion211/g/playground/static/playground/files/optimal_result_steps.txt")


#Extracting input from text files
with open('/home/rgalion211/g/playground/static/playground/files/tasks.txt') as f:

    while True:
        x = f.readline()

        if not x :
            break

        list = x.split(',')

        task = int(list[0])
        time[task] = int(list[1])


with open('/home/rgalion211/g/playground/static/playground/files/task_links.txt') as f:

    while True:

        x = f.readline()

        if not x:
            break

        list = x.split(',')

        task_1 = int(list[0])
        task_2 = int(list[1])
        link[task_1].append(task_2)



# create intinal population
def getpopulation ( popSize ) :

    solutions = []

    for _ in range(popSize) :

        solution = [ 0 , 1 ]

        for i in range(25):
            solution.append(0)

        for i in range(steps-1) :

            j = random.randint(2, 26)

            while solution[j] == 1 :
                j = random.randint(1, 26)

            solution[j] = 1

        solutions.append(solution)

    return solutions




#find the shift tasks by using dfs function
def DFS ( p , sol ) :

    is_visited[p] = True
    shift.append(p)

    for c in link[p] :
        if sol[c] == False and is_visited[c] == False :
            DFS(c,sol)


#using single point crossover to generate child
def singlepointcrossover ( sol1 , sol2 ) :

    index = random.randint(1, 26)
    sol3 = []

    for i in range(27) :

        if i < index :
            sol3.append(sol1[i])
        else :
            sol3.append(sol2[i])

    return sol3

#using swap mutaion to apply mutaion to child
def swapmutaion ( child ) :


    i1 = random.randint(1, 26)
    i2 = random.randint(1, 26)

    while ( child[i1] + child[i2] == 1 )  == False  :
        i1 = random.randint(1, 26)
        i2 = random.randint(1, 26)

    temp = child[i1]
    child[i1] = child[i2]
    child[i2] = temp



#find max time which is the fitness
def fit( sol ) :

    maximumTime = 0

    for i in range(1,27) :

        if  sol[i] == 1 :

            DFS(i,sol)

            shift_sum = 0

            for x in shift :
                shift_sum += time[x]

            maximumTime = max ( maximumTime , shift_sum )

            shift.clear()

    for i in range(1,27):
        is_visited[i] = False

    return maximumTime

#Write the solutions
def write( sol , file_name , text ) :

    total_differences = 0
    maximumTime = -1
    minimumTime = 10000000
    totalTime = sum(time)
    rate = totalTime/steps


    with open(file_name, 'a') as f:

        f.write(text)
        f.write('\n')

        for i in range(1,27) :

            if  sol[i] == 1 :

                DFS(i,sol)

                shift_sum = 0

                for x in shift :
                    shift_sum += time[x]


                f.write(str(shift))
                f.write('\n')
                f.write("total time = " + str(shift_sum) )
                f.write('\n')
                f.write("dif = " + str(abs(shift_sum - rate ) ) )
                f.write('\n')

                total_differences += abs(shift_sum - rate )

                maximumTime = max ( maximumTime , shift_sum )
                minimumTime = min ( minimumTime , shift_sum )

                shift.clear()

        for i in range(27) :
            is_visited[i] = False


        f.write("total time = " + str(totalTime ) )
        f.write('\n')
        f.write("total time / steps = " + str(rate) )
        f.write('\n')
        f.write("total differences = " + str(total_differences ) )
        f.write('\n')
        f.write("average differences = " + str(total_differences/steps) )
        f.write('\n')
        f.write("max time = "+ str(maximumTime) )
        f.write('\n')
        f.write("min time = " + str( minimumTime) )
        f.write('\n')
        f.write('.............................................................................................\n')






def start(popultaionSZ,maxIter,candidatesol):
  num = 1
  firstpopulation = getpopulation(popultaionSZ)

  bestStr=[]
  while maxIter > 0 :

      best = []

      for sol in firstpopulation :

          best.append((sol,fit(sol)))
          write(sol, '/home/rgalion211/g/playground/static/playground/files/all_results_steps.txt','iteration {} '.format(num))
          best.sort(key = lambda x:x[1] )

      newpopulation = []

      for _ in range(candidatesol):
          newpopulation.append(best[_][0])

      childsols = []

      for _ in range(popultaionSZ - candidatesol):

          id1 = random.randint(0, candidatesol-1)
          id2 = random.randint(0, candidatesol-1)

          child = singlepointcrossover(newpopulation[id1], newpopulation[id2])

          swapmutaion(child)

          childsols.append(child)

      newpopulation += childsols

      firstpopulation = newpopulation

      print("Best fitness from iteration number {} = {} ".format(num,best[0][1]) )
      bestStr.append("Best fitness from iteration number {} = {} ".format(num,best[0][1]))
      if maxIter == 1 :
              write(best[0][0], '/home/rgalion211/g/playground/static/playground/files/optimal_result_steps.txt',"Optimal solution")
      num +=1
      maxIter -= 1
  return bestStr
