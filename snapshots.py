import boto3
import datetime

today = datetime.datetime.today()
max_age = datetime.timedelta(7)

ec2 = boto3.client('ec2')
reservations = ec2.describe_instances()['Reservations']
for reservation in reservations:
	for instance in reservation['Instances']:
		instance_name = instance['Tags'][0]['Value']
		instance_id = instance['InstanceId']
		for volume in instance['BlockDeviceMappings']:
			volume_id = volume['Ebs']['VolumeId']
			print("Snapshot: i/" + instance_name + " v/" + volume_id)
			ec2.create_snapshot(Description=instance_name,VolumeId=volume_id)
			for snapshot in ec2.describe_snapshots(Filters=[{'Name':'volume-id','Values':[volume_id]}])['Snapshots']:
				age = today-snapshot['StartTime'].replace(tzinfo=None)
				if age > max_age:
					snapshot_id = snapshot['SnapshotId']
					print("Eliminando: " + snapshot_id + "(" + str(age) + ")")
					ec2.delete_snapshot(SnapshotId=snapshot_id)