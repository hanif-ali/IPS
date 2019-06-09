from django import forms

class VoterForm(forms.Form):
    voter_id = forms.IntegerField(min_value=1)
    grade = forms.CharField(max_length=10)
    name = forms.CharField(max_length=50)

    
def dynamicpollform(number_of_candidates_external):
    class PollForm(forms.Form):
        grade = forms.CharField(max_length=10)
        house = forms.CharField(max_length=10)
        category = forms.CharField(max_length = 10)
        number_of_candidates = forms.IntegerField(min_value=1)

        # Dynamically create ID fields according to number_of_candidates_external
        for i in range(number_of_candidates_external):
            exec("candidateid"+str(i)+" = forms.IntegerField(min_value=0)")
    return PollForm
