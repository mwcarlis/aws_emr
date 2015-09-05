#/usr/bin/python


def add_instance_group(client):
    response = client.add_instance_groups(
            InstanceGroups=[
                {
                    'Name': 'mattsattempt',
                    'Market': 'SPOT',
                    'InstanceRole': 'MASTER',
                    'BidPrice': '0.011',
                    'InstanceType': 't2.micro',
                    'InstanceCount': 1,
                    # 'Configurations': [
                    #     {
                    #         'Classification': 'core-site',
                    #         'Configurations': {'... recursive ...'},
                    #         'Properties': {
                    #             'string': 'string'
                    #         }
                    #     },
                    # ]
                }
            ],
            #          j-36OYZ5L6E8H41
            JobFlowId='j-25MAT5TW2C594'
    )
    return response

if __name__ == '__main__':
    pass

# job_run.stream_steps('My wordcount example',
#                      's3n://facedata/wordSplitter.py',
#                      'aggregate',
#                      's3n://facedata/word_18',
#                      's3n://facedata/output')
# instance_groups = []
# instance_groups.append(InstanceGroup(
#     num_instances=1,
#     role="MASTER",
#     type="m1.small",
#     market="ON_DEMAND",
#     name="My cluster2"))
# instance_groups.append(InstanceGroup(
#     num_instances=2,
#     role="CORE",
#     type="m1.small",
#     market="ON_DEMAND",
#     name="Worker nodes"))
# instance_groups.append(InstanceGroup(
#     num_instances=2,
#     role="TASK",
#     type="m1.small",
#     market="SPOT",
#     name="My cheap spot nodes",
#     bidprice="0.002"))

    #job_run.stream_steps('My wordcount example',
    #                     's3n://facedata/wordSplitter.py',
    #                     'aggregate',
    #                     's3n://facedata/word_18',
    #                     's3n://facedata/output/')

    #job_run.init_job_flows('My Jobflow 4',
                           #'s3n://facedata/logs/')
    # PERMIT = True
    # if not PERMIT:
    #     job_run.init_job_flows('My Jobflow 4',
    #                            's3n://facedata/logs')
    # # time_snap = datetime.datetime.now()
    # # hour_ago = time_snap.replace(hour_ago.hour - 1)
    # while True:
    #     print '\n\n\n'
    #     for cl in job_run.emr_conn.list_clusters().clusters[:4]:
    #         st = cl.status
    #         # print cl.name, cl.id, st.state
    #         print cl.id, st.state

    #     if not PERMIT:
    #         time.sleep(2)
    #     else:
    #         break



