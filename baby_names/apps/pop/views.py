from django.shortcuts import render, redirect, reverse
from ..faves.models import Frequency

# Create your views here.
def index(request):
	names = Frequency.objects.filter(state="CA",gender="M")[:10]
	# newNames = []
	# for i in range(0,10):
	# 	newNames.append(names[i])

	states = Frequency.objects.raw("select distinct state as id, state from frequency order by state")
	# print allStates
	# for s in allStates:
	# 	print s.state

	# states = [
	# 	{'name': 'AK'},
	# 	{'name': 'CA'}
	# 	]

	context = {
		'names': names,
		'states': states
	}
	return render(request, 'pop/index.html', context)

def filter(request):
	print "Running filter..."
	query = "SELECT name as id, name, sum(count) as count FROM frequency"
	whereclause = " WHERE id>0"
	groupby = " GROUP BY name ORDER BY sum(count) desc"
	name_dict = []

	if 'gender' in request.GET and request.GET['gender']!="":
		whereclause += " and gender=%s"
		name_dict.append(request.GET['gender'])
		# name_dict['gender'] = request.GET['gender']
	if request.GET['state']!="":
		whereclause += " and state=%s"
		name_dict.append(request.GET['state'])
		# name_dict['state'] = request.GET['state']
	if 'year' in request.GET:
		whereclause += " and year=%s"
		name_dict.append(request.GET['year'])
		# name_dict['year'] = request.GET['year']

	query+=whereclause+groupby
	print query, name_dict
	names = Frequency.objects.raw(query, name_dict)[:100]
	for n in names:
		print n.name, n.count
	return redirect(reverse('pop:index'))