import datetime as dt


# My Logger
# Default Path = my_project.log / you are free to insert your own path
def my_logger(path_n_file_name='my_project.log'):
    def log_main(func):
        # Formatting output
        def f_line(f, input_, output_a, output_k):
            return f"{dt.datetime.now().strftime('%H:%M on %B %d, %Y')} " \
                   f"| {f.__name__} | {input_} | {f(*output_a, **output_k)}"

        # Checking for directory to upload
        def log_fix(to_file_path: str, line: str):
            try:
                with open(to_file_path, mode='a') as file:
                    file.write(line + '\n')
            except (FileNotFoundError, NotADirectoryError) as er:
                print(f'{er}\nЗаданная {to_file_path} директория не существует! Перепроверьте пожалуйста ‼️')
                return False
            return True

        # Decorating
        def new_func(*args, **kwargs):
            if args == () and kwargs == {}:
                result = f_line(func, None, args, kwargs)
            elif args != () and kwargs == {}:
                result = f_line(func, args, args, kwargs)
            elif args == () and kwargs != {}:
                result = f_line(func, kwargs, args, kwargs)
            else:
                result = f_line(func, [args, kwargs], args, kwargs)
            log_fix(path_n_file_name, result)
            return func(*args, **kwargs)
        return new_func
    return log_main


@my_logger()
def a_plus_b(a, b):
    return a + b


if __name__ == '__main__':
    # # Testing
    # a_plus_b(1, 2)
    pass

