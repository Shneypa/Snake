import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(name = "Snake",

                options = {"build_exe":{"packages":["pygame"],
                "include_files":["icon.png","SnakeMenu.png",
                                "strawberry.png","snake_head.png"]}},

                description = "Snake game",
                executables = executables


                )