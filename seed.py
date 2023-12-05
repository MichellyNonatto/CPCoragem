
from servicos.models import Raca


def criar_dados():
    Raca.objects.create(nome='Siamês', especie='Gato')
    Raca.objects.create(nome='Persa', especie='Gato')
    Raca.objects.create(nome='Maine Coon', especie='Gato')
    Raca.objects.create(nome='Ragdoll', especie='Gato')
    Raca.objects.create(nome='Sphynx', especie='Gato')
    Raca.objects.create(nome='Bengal', especie='Gato')
    Raca.objects.create(nome='Abissínio', especie='Gato')
    Raca.objects.create(nome='Scottish Fold', especie='Gato')
    Raca.objects.create(nome='Gato-de-bengala', especie='Gato')
    Raca.objects.create(nome='Exótico de Pêlo Curto', especie='Gato')

    Raca.objects.create(nome='Labrador Retriever', especie='Cachorro')
    Raca.objects.create(nome='Golden Retriever', especie='Cachorro')
    Raca.objects.create(nome='Bulldog Francês', especie='Cachorro')
    Raca.objects.create(nome='Beagle', especie='Cachorro')
    Raca.objects.create(nome='Dachshund', especie='Cachorro')
    Raca.objects.create(nome='Poodle', especie='Cachorro')
    Raca.objects.create(nome='Boxer', especie='Cachorro')
    Raca.objects.create(nome='Shih Tzu', especie='Cachorro')
    Raca.objects.create(nome='Husky Siberiano', especie='Cachorro')
    Raca.objects.create(nome='Pastor Alemão', especie='Cachorro')


if __name__ == '__main__':
    criar_dados()
