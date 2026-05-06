# April 30, 2026
# Creating HTMl file from python

import random

stFile = open("./AdvancedTopics/Data/students.txt", "r")
outFile = open("./AdvancedTopics/main.html", "w")

students = [stu.strip("\n") for stu in stFile.readlines()]
random.shuffle(students)

names = stFile.readlines()
outFile.write("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Tennis Tournament</title>
                </head>
                <body>
                    <h1>Today's Matches</h1>
                    <div>
                        <table border="1">
                            <tr>
                                <th>Player 1</th>
                                <th>vs</th>
                                <th>Player 2</th>
                            </tr>
            """)

for i in range(0, len(students)-1, 2):
    outFile.write(f"""
                            <tr>
                                <th>{students[i]}</th>
                                <th>vs</th>
                                <th>{students[i+1]}</th>
                            </tr>
""")

outFile.write("""
                        </table>
                    </div>
                </body>
                </html>
            """)


stFile.close()
outFile.close()