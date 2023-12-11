
def somecheck():
    with open('sample.txt', 'rt', newline='', encoding='ascii', errors='replace') as f:
        print(f.read())
    import io

    for i in range(5):
        print(i, end=' ')

    with open('sample_binary_file.bin', 'wb') as f:
        # data = f.read()
        # f.write(b'Hi there')
        text = 'Hi There'
        f.write(text.encode('utf-8'))

    with open('sample_binary_file.bin', 'rb') as f:
        print(f.read())

    import os
    if not os.path.exists('sample.txt'):
        with open('sample.txt', 'wt') as f:
            f.write('You added here')
    else:
        with open('sample.txt', 'wt') as f:
            f.write('append')
            print('append done')

    with open('sample.txt', 'xb') as f:
        print(f.read())

    s = io.StringIO()

    s.write('Hello World\n')
    # print(z)

    print('This is a test', file=s)
    print('xx', s.getvalue())

    return

def manipulate_path():
    import os
    path = '/home/akash/sample.txt'

    print(os.path.basename(path))
    print(os.path.dirname(path))
    print(os.path.join('tmp', 'data', os.path.basename(path)))
    print(os.path.splitext(path))
    print(os.path.getsize(path))
    pass

manipulate_path()