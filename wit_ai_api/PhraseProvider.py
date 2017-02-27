# -*- coding: UTF-8 -*-

from EntityType import EntityType

class PhraseProvider:

	def __init__(self, requirements):
		responseData = requirements.getResponseData();

		self.quantity = responseData[EntityType.NUMBER_OF_PHRASES.value].getValue();
		self.typeOf = responseData[EntityType.TYPE_OF_PHRASE.value].getValue()
		self.phraseRepository = {
			"amor": [
				"Si yo fuese el mar, y tu una roca, haría subir la marea, para besar tu boca.",
				"Un hombre quiere ser el primer amor de su amada. Una mujer quiere que su amado sea su último amor.",
				"Te quiero no solo por como eres, sino por como soy yo cuando estoy contigo.",
				"Un día dejé caer una lágrima en el océano. El día que la encuentre será el día que deje de quererte.",
				"Sabes que estás enamorado cuando no quieres dormir por la noche, porque tu vida real supera a tus sueños."],
			"amistad": [
				"Un amigo es uno que lo sabe todo de ti y a pesar de ello te quiere.",
				"La amistad es más difícil y más rara que el amor. Por eso, hay que salvarla como sea.",
				"El que busca un amigo sin defectos se queda sin amigos.",
				"Los verdaderos amigos se tienen que enfadar de vez en cuando.",
				"La amistad duplica las alegrías y divide las angustias por la mitad."],
			"motivacional": [
				"Sólo una cosa convierte en imposible un sueño: el miedo a fracasar.",
				"Cuando alguien desea algo debe saber que corre riesgos y por eso la vida vale la pena.",
				"Los días más perdidos de tu vida son los que no has sonreído.",
				"Para que los cambios tengan un valor verdadero deben ser consistentes y duraderos.",
				"Ponte de frente al sol y las sombras quedarán detrás de ti."],
			"chistosa": [
				"Mi psiquiatra me dijo que estaba loco y pedí una segunda opinión. Me dijo que también era feo.",
				"Los hombres son como cuentas bancarias. Cuanto más dinero, más interés generan.",
				"Si pudieses patear a la persona responsable de la mayoría de tus problemas, no podrías sentarte en un mes.",
				"La gente que piensa que saben todo son una gran molestia para la que si lo sabemos todo.",
				"Un día sin sol es, ya sabes, la noche."],
			"inspiradora": [
				"Todos nuestros sueños pueden hacerse realidad si tenemos el coraje de perseguirlos.",
				"No tener tiempo es una excusa para no comprometerse.",
				"Si quieres conseguir algo que nunca has conseguido tendrás que hacer cosas que nunca has hecho.",
				"Hecho, es 10 veces mejor que perfecto.",
				"Problema=Oprtunidad."]
		 }

	def provide(self):
		if self.typeOf in list(self.phraseRepository.keys()):
			if self.quantity <= len(self.phraseRepository[self.typeOf]):
				return self.phraseRepository[self.typeOf][:self.quantity]
		else:
			return ["Categoria " + self.typeOf + " no disponible."]

	def printPhrases(self):
		phrases = self.provide()
		print("\nFrases recomendadas para ti: ")
		for phrase in phrases:
			print("\t-> " + phrase)
