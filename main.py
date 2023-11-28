import dumperClass


def main():
    tokens = []

    for token in tokens:
        dumper = dumperClass.VkGroupDumper(token)
        dumper.dump_all()


if __name__ == "__main__":
    main()
