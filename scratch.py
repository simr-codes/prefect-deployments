from prefect import flow, task, variables
from prefect.blocks.system import String


@task(log_prints=True, retries=4)
def add_one(x: int):
    return x + 1


@flow(
    retries=5,
    name="scratch-I",
    description="a scratch flow",
    persist_result=True,
    log_prints=True,
)
def main():
    string_block = String.load("string-block")
    # with a default value
    greets_from_prefect = variables.get("greets", default="Hey")
    print(greets_from_prefect)
    # 42

    for x in [1, 2, 3]:
        first = add_one(x)
        print(first)
        second = add_one(first)
        print(second)
        print("💪💪💪")
        print("💪💪💪", string_block.value)


if __name__ == "__main__":
    ##run it & then creates a deployment
    # main()
    # create your first deployment to automate your flow
    # To transition from persistent infrastructure to dynamic infrastructure, use flow.deploy instead of flow.serve.
    main.deploy(
        work_pool_name='managed-work-pool',
        # build=False,
        # image='/home/simr/Desktop/prefect/scratch.py',
        name="scratch-I",
        interval=120,
        # cron="* * * * *",
        # tags=["scratch"],
        # tags=["testing", "tutorial"],
        description="""scratch-I""",
        #    ,parameters=
        # version="tutorial/deployments",
    )
